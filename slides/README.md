# KubeCon Markdown slides

Open [kubecon-genai.md](kubecon-genai.md). Slides are separated by `---`.
Use a Markdown slide renderer with Mermaid support, including `xychart-beta`.
The deck is Markdown source, not a rendered PowerPoint or PDF.

Speaker notes are omitted. TODOs remain in the slide source.
Sources and qualifications are collected in [sources.md](sources.md).

## Assets and evidence

- `assets/python-genai-contributions-monthly.svg`: monthly non-bot merged PRs in Python GenAI since launch.

- `assets/aspire-genai-conversation-long.png`: final inference with the question, tool calls, results, and answer.
- `assets/aspire-inference-attributes.png`: attributes table of the first inference span.
- `assets/otel-inference-attributes.json`: complete captured attribute values for that span.
- `assets/semconv-waterfall.svg`: operation coverage, stability targets, and core convention boundaries.
- `assets/expected-waterfall.svg`: intended span names and nesting, illustrative timing.
- `assets/usage-vs-bill.svg`: imaginary live cost estimate and delayed provider billing.
- `assets/aspire-waterfall.png`: actual happy-case waterfall, light mode, all 22 spans.
- `assets/aspire-parent-gap.svg`: full trace with a boxed runbook subtree and two arrows marking intended parents.
- `assets/aspire-orphan-http.png`: the detached runbook HTTP span in a separate trace.
- `assets/aspire-trace.png`: earlier single-service hierarchy crop, not used in the deck.
- `assets/conformance-inference.png`: live dashboard, filtered to Anthropic.
- `assets/conformance-findings.png`: archived capture, not used in the deck.
- `queries/01-semconv.sql`: exact first on-slide query.
- `queries/02-mixed.sql`: exact on-slide mapping query.
- [Full ancestry query](../demos/kubecon-genai/queries/02-normalized.sql): optional backup for the parentage discussion.
- [Sources and presentation caveats](sources.md).

Screenshot trace: `b2fb5dc7fc85244d41a7f3667beaec03`.
Both slide queries were executed against this capture: 2 / 280 and 5 / 900; the latter double-counts the Anthropic inference.
Queries use the SQLite `span_data` view, with attributes exposed as quoted columns.
The screenshots are saved locally so the deck does not depend on live services.
The waterfall excludes unused dashboard space and preserves every trace row.

## Live demo fallback

From `demos/kubecon-genai`:

```sh
docker compose up --build -d
curl --fail-with-body http://localhost:8000/run \
  -H 'Content-Type: application/json' -d '{"scenario":"mixed"}'
python3 inspect_demo.py
```

Use the captured screenshot if the live demo fails. The deck describes the
current workflow and isolated LangSmith runbook services.
