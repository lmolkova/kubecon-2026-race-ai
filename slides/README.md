# KubeCon Markdown slides

Open [kubecon-genai.md](kubecon-genai.md). Slides are separated by `---`.
Use a Markdown slide renderer with Mermaid support, including `xychart-beta`.
The deck is Markdown source, not a rendered PowerPoint or PDF.

## Presentation mode

From the repository root, run:

```sh
python -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765/slides/ in a browser. Use the arrow keys to
change slides and **F** or **Full screen** for presentation mode.
Elements with `class="fragment"` appear one at a time as you advance;
going back into a slide shows all of them. Fragments with the same
`data-fragment` value appear together.
The viewer loads the Markdown source and local assets directly.
Internet access to `cdn.jsdelivr.net` is required for the Markdown and
Mermaid renderers and syntax highlighting. SQL, JSON, Python, shell, and PromQL code use highlight.js
with light colors. All slides use light backgrounds regardless of system theme.
Reload the page after editing the source.
Stop the server with **Ctrl+C**.

Speaker notes are omitted. TODOs remain in the slide source.
Sources and qualifications are collected in [sources.md](sources.md).

## Colors

The cover and two transition slides use artwork extracted from the supplied
KubeCon + CloudNativeCon North America 2026 PowerPoint template. The navy logo
and pale blue background keep these slides light. The original PowerPoint is
preserved in `assets`; `<!-- layout: branded-transition -->` selects this layout.

Diagram and chart colors follow the OpenTelemetry logo. OTel blue `#425cc7`
is the main series color and marks diagnostic-agent spans. OTel amber
`#f5a800` marks runbook spans. Teal `#0f8188` marks OpenInference and the
provider bill, and plum `#a3367a` marks LangSmith OTLP. Red is reserved for
broken context.

## Assets and evidence

- `assets/python-genai-contributions-monthly.svg`: monthly non-bot merged PRs to Python GenAI instrumentation, stacked by repository (python-contrib in grey, python-genai in OTel blue), with a marker at the May 12, 2026 repository launch.

- `assets/aspire-genai-conversation-long.png`: final inference with the question, tool calls, results, and answer. Slide 15 shows these messages in an Aspire-style HTML mockup.
- `assets/aspire-inference-attributes.png`: Aspire's attributes table for the first inference span. Slide 13 shows these values as an HTML table.
- `assets/otel-inference-attributes.json`: complete captured attribute values for that span.
- `assets/semconv-waterfall.svg`: operation coverage, stability targets, and core convention boundaries.
- `assets/expected-waterfall.svg`: intended span names and nesting, with approximate timing aligned to the saved capture, matching service colours and span markers, and an enlarged layout.
- `assets/usage-vs-bill.svg`: imaginary live cost estimate and delayed provider billing.
- `assets/aspire-waterfall.svg`: vector redraw of the saved happy-case capture, preserving all 22 spans, nesting, resources, and markers, with original duration values in SVG metadata.
- `assets/aspire-waterfall.png`: original Aspire capture in light mode, retained as evidence.
- `assets/aspire-parent-gap.svg`: the same 22-span redraw with a boxed runbook subtree, two intended-parent arrows, and the separate orphan trace on its own time scale.
- `assets/aspire-orphan-http.png`: original capture of the detached runbook HTTP span in a separate trace.
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
Slides 3, 4, 9, and 12 share an SVG waterfall layout.
The images omit titles, capture summaries, footer captions, and per-span
duration columns; time axes and parentage annotations remain.
The captured views preserve every displayed trace row; bar shapes follow the
saved screenshot pixels, not recovered start/end timestamps.
Slide 3's names and nesting remain illustrative; its bar positions follow the
saved capture on the same 0–0.7 s axis. Slide 12's operation-coverage example
remains illustrative.

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
