"""Exercise the local services and compare telemetry with mock request records."""

import json
import os
import urllib.error
import urllib.request

from aspire_capture import capture, ground_truth, open_database, query as run_query

OTEL = os.getenv("DEMO_INSTRUMENTATION") == "otel"
db = open_database()


def query(name, trace_id):
    return run_query(db, name, trace_id)


for scenario in ("mixed", "tool-error"):
    request = urllib.request.Request(
        os.getenv("DEMO_URL", "http://localhost:8000") + "/run",
        data=json.dumps({"scenario": scenario}).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        response = urllib.request.urlopen(request, timeout=30)
    except urllib.error.HTTPError as exc:
        response = exc
    with response:
        result = json.load(response)
        assert response.status == (502 if scenario == "tool-error" else 200), result

    result["trace_id"] = capture(db, run_id=result["run_id"],
                                 expected_calls=5 if scenario == "mixed" else 3)

    http_spans = list(db.execute(
        "SELECT scope,kind FROM spans WHERE trace_id=?", (result["trace_id"],)))
    assert any(row["scope"] == "opentelemetry.instrumentation.fastapi" and row["kind"] == "SERVER"
               for row in http_spans), http_spans
    assert any(row["scope"] == "opentelemetry.instrumentation.httpx" and row["kind"] == "CLIENT"
               for row in http_spans), http_spans
    assert all(row["scope"] != "demo.http" for row in http_spans), http_spans
    assert not db.execute(
        "SELECT 1 FROM spans WHERE trace_id=? AND scope='opentelemetry.instrumentation.fastapi' "
        "AND kind='INTERNAL'", (result["trace_id"],)
    ).fetchone(), "Unexpected ASGI receive/send spans"

    truth = ground_truth(result["run_id"])
    simple = query("01-semconv.sql", result["trace_id"])[0]
    normalized = query("02-normalized.sql", result["trace_id"])
    totals = {key: sum(row[key] or 0 for row in normalized)
              for key in ("model_calls", "input_tokens", "output_tokens")}
    if not OTEL:
        framework_spans = list(db.execute(
            "SELECT name,attrs FROM spans WHERE trace_id=? AND scope='openinference.instrumentation.langchain'",
            (result["trace_id"],)))
        assert {"diagnose_workload", "diagnostic", "model", "tools", "inspect_workload", "ChatOpenAI"} <= {
            row["name"] for row in framework_spans}, framework_spans
    if scenario == "mixed":
        if not OTEL:
            assert "runbook" not in {row["name"] for row in framework_spans}
            assert db.execute("""
                SELECT 1 FROM spans model
                JOIN spans step ON model.parent_id=step.span_id
                JOIN spans agent ON step.parent_id=agent.span_id
                WHERE model.trace_id=? AND model.scope='langsmith' AND model.name='ChatOpenAI'
                  AND step.scope='langsmith' AND step.name='model'
                  AND agent.scope='langsmith' AND agent.name='runbook'
            """, (result["trace_id"],)).fetchone(), "LangSmith model must belong to the LangSmith runbook agent"
        assert truth == dict(attempts=4, successes=4, input_tokens=700, output_tokens=160), truth
        expected_simple = dict(model_calls=5, input_tokens=900, output_tokens=210) if OTEL else dict(model_calls=2, input_tokens=280, output_tokens=70)
        assert simple == expected_simple, simple
        assert totals == dict(model_calls=5, input_tokens=900, output_tokens=210), totals
        assert {row[0] for row in db.execute(
            "SELECT DISTINCT service FROM spans WHERE trace_id=?", (result["trace_id"],)
        )} == {"diagnostic-agent", "runbook"}
        assert not db.execute("""
            SELECT 1 FROM spans WHERE trace_id=? AND service='runbook'
              AND scope IN ('openinference.instrumentation.langchain', 'com.anthropic.sdk.python')
        """, (result["trace_id"],)).fetchone()
        if not OTEL:
            assert {row["model"]: row["main_agent"] for row in normalized} == {
                "gpt-6.1-sol": None, "claude-sonnet-5-5": None, "gpt-6-luna": None
            }, normalized
            # Preserve the observed callback-to-OTel context gap in the baseline.
            assert {row["tool"] for row in normalized} == {None, "inspect_workload"}, normalized
    else:
        assert truth == dict(attempts=2, successes=1, input_tokens=120, output_tokens=30), truth
        errors = db.execute("SELECT name FROM spans WHERE trace_id=? AND status='ERROR'",
                            (result["trace_id"],)).fetchall()
        assert {"POST /run", "anthropic.messages.create"} <= {row["name"] for row in errors}, errors
    if OTEL:
        spans = {row["span_id"]: dict(row) for row in db.execute(
            "SELECT * FROM spans WHERE trace_id=?", (result["trace_id"],))}
        scopes = {span["scope"] for span in spans.values()}
        assert not any("openinference" in scope or "langsmith" in scope for scope in scopes), scopes
        assert "opentelemetry.instrumentation.genai.langchain" in scopes, scopes
        assert "com.anthropic.sdk.python" in scopes, scopes
        if scenario == "mixed":
            assert "opentelemetry.instrumentation.genai.openai" in scopes, scopes
        agents = [span for span in spans.values()
                  if span["name"] == "invoke_agent diagnostic"]
        assert len(agents) == 1, agents
        agent = agents[0]
        assert json.loads(spans[agent["parent_id"]]["attrs"]).get("gen_ai.tool.name") == "inspect_workload"
        native = next(span for span in spans.values()
                      if span["scope"] == "com.anthropic.sdk.python")
        framework = spans[native["parent_id"]]
        assert framework["name"] == "chat claude-sonnet-5-5", framework
        assert framework["parent_id"] == agent["span_id"], framework
        for span in spans.values():
            attrs = json.loads(span["attrs"])
            if attrs.get("gen_ai.operation.name") != "chat":
                continue
            if span["status"] != "ERROR":
                assert attrs.get("gen_ai.input.messages"), span
                assert attrs.get("gen_ai.output.messages"), span
            ancestors = []
            parent = span["parent_id"]
            while parent:
                ancestor = spans[parent]
                ancestors.append(ancestor)
                parent = ancestor["parent_id"]
            model = attrs.get("gen_ai.request.model")
            expected_tool = {"claude-sonnet-5-5": "inspect_workload", "gpt-6-luna": "consult_runbook"}.get(model)
            if expected_tool:
                assert any(json.loads(a["attrs"]).get("gen_ai.tool.name") == expected_tool
                           for a in ancestors), (model, [a["name"] for a in ancestors])

    print(json.dumps({"scenario": scenario, "trace_id": result["trace_id"],
                      "run_id": result["run_id"], "ground_truth": truth,
                      "simple": simple, "normalized": totals, "status": "PASS"}), flush=True)

db.close()
