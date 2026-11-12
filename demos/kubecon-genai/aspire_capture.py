"""Read Aspire's OTLP JSON into a query-local SQLite database."""

import json
import os
import sqlite3
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
DASHBOARD = os.getenv("ASPIRE_URL", "http://localhost:18888")
API_KEY = os.getenv("ASPIRE_API_KEY", "local-demo-dashboard-api-key")
ROUTER = os.getenv("MODEL_URL", "http://localhost:8001")


def get_json(url, headers=None):
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=10) as response:
        return json.load(response)


def value(item):
    if "arrayValue" in item:
        return [value(v) for v in item["arrayValue"].get("values", [])]
    if "kvlistValue" in item:
        return attributes(item["kvlistValue"].get("values", []))
    if "intValue" in item:
        return int(item["intValue"])
    return next(iter(item.values()), None)


def attributes(items):
    return {item["key"]: value(item["value"]) for item in items}


def open_database(path=":memory:"):
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript((ROOT / "capture-schema.sql").read_text())
    return db


def import_spans(db, payload):
    data = payload.get("data", payload)
    for resource in data.get("resourceSpans", []):
        service = attributes(resource.get("resource", {}).get("attributes", [])).get("service.name", "unknown")
        for scope in resource.get("scopeSpans", []):
            for span in scope.get("spans", []):
                kind = span.get("kind", 0)
                status = span.get("status", {}).get("code", 0)
                db.execute("INSERT OR REPLACE INTO spans VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
                    span["traceId"], span["spanId"], span.get("parentSpanId") or None,
                    service, scope.get("scope", {}).get("name", ""), span["name"],
                    {0: "UNSPECIFIED", 1: "INTERNAL", 2: "SERVER", 3: "CLIENT", 4: "PRODUCER", 5: "CONSUMER"}.get(kind, str(kind).removeprefix("SPAN_KIND_")),
                    {0: "UNSET", 1: "OK", 2: "ERROR"}.get(status, str(status).removeprefix("STATUS_CODE_")),
                    int(span["startTimeUnixNano"]), int(span["endTimeUnixNano"]),
                    json.dumps(attributes(span.get("attributes", []))),
                    json.dumps(span.get("events", [])),
                ))
    db.commit()


def capture(db, run_id=None, trace_id=None, expected_calls=None, timeout=30):
    deadline = time.monotonic() + timeout
    previous = None
    unchanged_since = time.monotonic()
    while time.monotonic() < deadline:
        path = f"/api/telemetry/traces/{trace_id}" if trace_id else "/api/telemetry/spans?limit=10000"
        try:
            payload = get_json(DASHBOARD + path, {"X-API-Key": API_KEY})
        except urllib.error.HTTPError as exc:
            if exc.code != 404 or not trace_id:
                raise
            time.sleep(0.5)
            continue
        import_spans(db, payload)
        if not trace_id:
            server = db.execute("""
                SELECT trace_id FROM span_data WHERE kind='SERVER' AND name='POST /run'
                AND (:run_id IS NULL OR demo_run_id=:run_id)
                ORDER BY start_ns DESC LIMIT 1
            """, {"run_id": run_id}).fetchone()
            if server:
                trace_id = server["trace_id"]
            time.sleep(0.5)
            continue
        count = db.execute("SELECT count(*) FROM spans WHERE trace_id=?", (trace_id,)).fetchone()[0]
        calls = sum(row["model_calls"] for row in query(db, "02-normalized.sql", trace_id))
        missing_parents = db.execute("""
            SELECT count(*) FROM spans s LEFT JOIN spans p
              ON s.trace_id=p.trace_id AND s.parent_id=p.span_id
            WHERE s.trace_id=? AND s.parent_id IS NOT NULL AND p.span_id IS NULL
        """, (trace_id,)).fetchone()[0]
        if count != previous:
            previous, unchanged_since = count, time.monotonic()
        if count and not missing_parents and time.monotonic() - unchanged_since >= 2:
            if expected_calls is None or calls == expected_calls:
                return trace_id
        time.sleep(0.5)
    raise TimeoutError("Timed out waiting for complete telemetry from Aspire")


def query(db, filename, trace_id):
    return [dict(row) for row in db.execute(
        (ROOT / "queries" / filename).read_text(), {"trace_id": trace_id})]


def ground_truth(run_id):
    records = get_json(ROUTER + "/requests/" + urllib.parse.quote(run_id, safe=""))
    return {
        "attempts": len(records), "successes": sum(r["status"] == 200 for r in records),
        "input_tokens": sum(r["input_tokens"] or 0 for r in records),
        "output_tokens": sum(r["output_tokens"] or 0 for r in records),
    }
