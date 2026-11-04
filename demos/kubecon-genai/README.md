# One request, several telemetry conventions

A Python LangGraph workflow calls local mock model APIs. Real instrumentations send
traces, logs, and metrics to Aspire. No cloud account or model credentials needed.

Model IDs: `gpt-4.1` for the agent, `claude-sonnet-4-6` for workload inspection,
and `gpt-4.1-mini` for runbook advice. Responses and usage are local fixtures.
Dependencies are locked in `uv.lock` and `runbook/uv.lock`; Aspire is pinned by image digest.

## Instrumentation

- OTel FastAPI and HTTPX instrument HTTP requests and propagation automatically.
- OpenInference instruments the workflow, diagnostic agent, graph steps, tools, and LangChain models.
- Anthropic SDK supplies native model tracing in the diagnostic tool, using the registered OTel provider.
  No third-party Anthropic instrumentor or manual spans are used.
- LangSmith traces the LangGraph runbook agent and its OpenAI inference through its OTel mode.
- Standard Python log messages use the configured OTel logging handler.
- HTTP metrics come from the HTTP instrumentations. There are no custom metrics.

`diagnostic-agent` runs the LangGraph workflow and diagnostic agent. Its runbook tool
calls `runbook` over HTTP. The runbook has its own image and lockfile, with
no OpenInference or Anthropic packages. LangSmith traces
its LangGraph graph, model step, and OpenAI call. Standard OTel FastAPI instrumentation
handles the HTTP boundary and incoming context. Aspire and the mock model API
run in separate containers. Four successful calls return 700 input tokens and
160 output tokens in total.

There are no hand-written spans, context bridges, propagation suppression, or
manual span attributes. FastAPI's separate built-in telemetry is disabled to
avoid duplicate HTTP instrumentation. SDK/exporter setup lives in `telemetry.py`.
Compose sets the OTLP endpoint, metric export interval, and service names.
Exporters and the metric reader read those environment variables directly.
LangSmith tracing is disabled in the workflow service and enabled throughout
the runbook service. No per-call tracing switches or manual context bridges
are needed. The OpenAI SDK has no additional inference instrumentor.

## Start

From this directory:

```sh
docker compose up --build -d
curl --fail http://localhost:8000/health
curl --fail-with-body http://localhost:8000/run \
  -H 'Content-Type: application/json' -d '{"scenario":"mixed"}'
python3 inspect_demo.py
```

Open [Aspire](http://localhost:18888). Published ports bind only to localhost.
Allow a few seconds for background export. The inspection script prints the
trace link and the two SQL results. It reads Aspire's authenticated telemetry API;
`ASPIRE_URL` and `ASPIRE_API_KEY` override the local demo defaults. It needs only
Python's standard library, not the application's dependencies.

Use `python3 inspect_demo.py --run-id <run-id>` for a specific request, or
`--trace-id <trace-id>` for a trace already in Aspire. Without either option,
it selects the latest `POST /run`. `--db output/telemetry.sqlite` keeps a local copy.
The model-router's `/requests/<run-id>` endpoint supplies independent request
totals for verification; it stores only in-memory fixture records.

The application returns a run ID as an HTTP response header. Configured automatic
header capture lets the inspection script find the server trace without calling
the OTel API inside the application. The same run ID links mock request records.
It is not used to rewrite parent relationships or stitch traces together.

## Parallel OTel demo

`compose.otel.yaml` runs the same `demo.py` and `runbook_service.py` with a separate
Compose project, network, dashboard, and ports. `instrumentation.py` selects the
instrumentation from Compose configuration:

| Service | Original | OTel variant |
| --- | --- | --- |
| Workflow and diagnostic | OpenInference LangChain | OTel GenAI LangChain |
| Diagnostic inference | Native Anthropic | Native Anthropic |
| Runbook graph | LangSmith | OTel GenAI LangChain |
| Runbook inference | LangSmith OpenAI wrapper | OTel GenAI OpenAI |

The OTel image has no OpenInference instrumentation. LangSmith is a transitive
LangChain dependency, but tracing is off by default and its wrapper is not used.
The application SDK and framework versions match the original workflow lockfile.
OTel dependencies are locked separately in `otel/uv.lock`.

```sh
docker compose -f compose.otel.yaml up --build -d
curl --fail-with-body http://localhost:8010/run \
  -H 'Content-Type: application/json' -d '{"scenario":"mixed"}'
ASPIRE_URL=http://localhost:18889 MODEL_URL=http://localhost:8011 \
  python3 inspect_demo.py
```

Open the second [Aspire dashboard](http://localhost:18889). The original stays
at port 18888. OTel content capture uses
`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_AND_EVENT` in both services;
Anthropic uses its native content-mode setting. No manual spans or context fixes
are added. The simple query now counts five inference spans and 900 input tokens: the
LangChain model span and native Anthropic span both report the same inference.

```sh
DEMO_INSTRUMENTATION=otel DEMO_URL=http://localhost:8010 \
  ASPIRE_URL=http://localhost:18889 MODEL_URL=http://localhost:8011 \
  python3 verify_demo.py
docker compose -f compose.otel.yaml down
```

Verification checks both successful and failed model calls, content capture,
instrumentation scopes, and the tool ancestry of each nested model call.

Verified traces:

- [OTel happy case](http://localhost:18889/traces/detail/3068f6c46578e4485a8386ccd3480cf1)
- [Original happy case](http://localhost:18888/traces/detail/1cc6a4208d3eb0c4fde39d852642e57b)

The diagnostic uses `create_agent` with `ChatAnthropic`. The OTel subtree is:

```text
execute_tool inspect_workload
└── invoke_agent diagnostic
    └── chat claude-sonnet-4-6
        └── anthropic.messages.create
```

Both inference spans report the same 200 input and 50 output tokens. Four provider
calls therefore produce five inference spans and summed usage of 900 input and
210 output tokens. The query intentionally does not deduplicate this overlap.
The original setup also records both OpenInference's `ChatAnthropic` span and
Anthropic's native span, but the native span still bypasses the agent/tool context.

The earlier plain nested `StateGraph` was omitted by OTel's classification rules.
This is tracked by [issue #578](https://github.com/open-telemetry/opentelemetry-python-genai/issues/578)
and [fix PR #617](https://github.com/open-telemetry/opentelemetry-python-genai/pull/617),
both open when checked on November 3, 2026. The demo uses published packages,
not the PR branch. `runbook` remains a workflow.

## What goes wrong

With OpenInference's optional GenAI dual-write off by default, `01-semconv.sql` finds
Anthropic and LangSmith: two calls, 280 input tokens, and 70 output tokens.
`02-normalized.sql` recognizes OpenInference too, but double-counts Anthropic:
five inference spans, 900 input tokens, and 210 output tokens. Aspire is not a SQL database; these queries run against
spans fetched from Aspire's HTTP telemetry API into query-local SQLite.

Queries use `span_data`, a view exposing attribute names as quoted SQL columns.
JSON extraction lives in the storage layer. The view also works with existing
captures and preserves missing values as NULL.

`diagnose_workload` calls GPT-4.1, dispatches tools, then calls GPT-4.1 again.
The tools invoke a `create_agent` diagnostic and a remote LangGraph `runbook`.
LangSmith automatically traces the runbook graph; `wrap_openai` captures its model.
There is no extra coordinator agent around the workflow.

Native Anthropic spans bypass the diagnostic agent. LangSmith nests the model
under the runbook, but the runbook bypasses its outer tool. LangSmith records
the runbook as `chain`, which the query does not classify as an agent.
The two GPT-4.1 calls belong directly to the workflow, which OpenInference
classifies as `CHAIN`; their null agent ancestry is expected.
Normalization alone neither deduplicates inference spans nor repairs missing ancestry.
HTTPX instrumentation is also enabled in runbook. In the OTel variant, its HTTP
client span is a child of `chat gpt-4.1-mini`. In the LangSmith baseline, the HTTP
client span was exported in a different trace with an unexported parent.
This is observed behavior in the locked versions, not an injected tracing fault.

LangSmith exports GenAI usage fields but names its inference span `ChatOpenAI`.
Anthropic names its span `anthropic.messages.create`. Inspect both alongside OpenInference's
`llm.*` fields. No claim is made that OpenInference lacks a GenAI opt-in.

## Model failure

```sh
curl --fail-with-body http://localhost:8000/run \
  -H 'Content-Type: application/json' -d '{"scenario":"tool-error"}'
```

The first mock response requests only the diagnostic tool. Its Anthropic model call
returns HTTP 503 with retries disabled. The application returns HTTP 502 and logs
the exception. Automatic instrumentations report errors. The failed inference
has no token usage; the normalization query reports missing usage separately.

## Verify and stop

```sh
python3 verify_demo.py
docker compose down
```

Verification checks both scenarios against independent mock request totals,
checks the instrumentation scopes, and preserves the observed missing ancestry.
Application services have no database or shared volume. The query tool uses an
in-memory SQLite database by default; `--db output/telemetry.sqlite` saves a local
copy. Aspire telemetry and model-router request records are lost on restart.
