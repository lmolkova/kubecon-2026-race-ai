# Sources and notes

## Demo evidence: slides 3–9, 14

- Code: [demo](../demos/kubecon-genai/demo.py), [locked versions](../demos/kubecon-genai/uv.lock).
- Main trace: `b2fb5dc7fc85244d41a7f3667beaec03`.
- Orphan trace: `01a1a3cdcf8a74568f6fdd9c7c86e09f`, HTTP span `f88b071f40ee83f4`.
- Two application services; local mocks; four successful model requests.
- Model IDs: `gpt-4.1`, `claude-sonnet-4-6`, and `gpt-4.1-mini`.
- Aspire screenshots recaptured in light mode on November 3, 2026; full waterfall and a separate orphan HTTP trace; boxes and arrows are SVG overlays.
- The query tool fetches OTLP JSON from Aspire into local SQLite without renaming or reparenting spans.
- Two GPT-4.1 calls: 420 input / 90 output tokens, OpenInference schema.
- ChatAnthropic also emits an OpenInference inference span: 200 / 50, duplicating the native Anthropic usage.
- Native Anthropic: 200 / 50; LangSmith wrapper: 80 / 20, both GenAI usage fields.
- OpenInference GenAI dual-write is off by default in the locked version.
- LangSmith automatically traces the runbook LangGraph graph and its model with `wrap_openai`; OpenInference instruments the LangGraph workflow, diagnostic agent, and tools.
- LangSmith recording is enabled for the entire isolated runbook service; no manual OTel context bridge exists. OTel FastAPI handles its HTTP boundary; OpenInference is not installed there.
- Anthropic combines HTTP and GenAI fields; Aspire's display label is not the raw span name.
- The compact mapping SQL handles this fixture, not arbitrary versions or duplicate instrumentation.
- `missing_usage` preserves absent usage; `SUM` does not turn it into measured zero.
- Ancestry: GPT-4.1 belongs directly to the workflow. Anthropic bypasses its diagnostic agent. LangSmith preserves runbook-to-model parenting, but the runbook bypasses its tool. The query does not classify LangSmith's `chain` as an agent, so classified agent ancestry remains null; the OpenInference ChatAnthropic span retains inspect_workload ancestry, while the native span does not.
- HTTPX is enabled in runbook. Its outgoing HTTP span is exported in the separate trace above with an unexported parent; the blue arrow marks the intended ChatOpenAI parent.
- HTTP metrics and ordinary application logs are not evidence of GenAI signal parity.
- Slide 6 is an illustrative cost chart, not captured telemetry or billing. Both series use USD by usage date; provider data has an invented one-day delay. The demo's 60% missing input tokens does not imply 60% missing cost.

## Conventions and development: slides 11–19, 23–25

- [GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai).
- [Reference scenario policy](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/AGENTS.md), and [reference contribution guide](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/reference/CONTRIBUTING.md).
- [Python GenAI](https://github.com/open-telemetry/opentelemetry-python-genai).
- [Python releases](https://github.com/open-telemetry/opentelemetry-python-genai/releases).
- [Migration and native instrumentation tracking](https://github.com/open-telemetry/opentelemetry-python-genai/issues/141).
- [JS migration](https://github.com/open-telemetry/opentelemetry-js-contrib/issues/3668).
- [Saved research](../kubecon-talk-research.md) contains counts, full weekly series, contributor methodology, and scoped JS PRs.

Contributor/release statistics use the November 1, 2026 research snapshot.
Python: 358 merged PRs since repository creation on May 12; 47 PR authors;
24 first merged-PR contributors to the OTel organization. JS AI work: 15 merged
PRs, 8 authors, 2 additional newcomers. Combined distinct authors: 53; newcomers: 26.
The weekly chart includes the partial first and last weeks; the mean excludes them.
Four coordinated Python beta release rounds plus patches; 13 released packages.
Refresh counts before presenting. They are not live dashboard values.

The roadmap is direction, not a delivery commitment. Separate established
signal definitions, active stabilization, and proposed extensions verbally.
Do not imply that planning, arbitrary steps, or every signal has stable coverage.

## Conformance: slides 20–22

- [Comparison dashboard](https://open-telemetry.github.io/semantic-conventions-conformance/#?q=anthropic).
- [Native Anthropic report](https://open-telemetry.github.io/semantic-conventions-conformance/#/target/gen-ai/python/anthropic/native).
- [Conformance repository](https://github.com/open-telemetry/semantic-conventions-conformance).
- [Weaver](https://github.com/open-telemetry/weaver).

Screenshots were captured for this deck on November 1, 2026, client local date.
The live dashboard identifies GenAI registry revision `9ffc7e00c639`.
This differs from the earlier pinned report in the research document.
Use the screenshots as a dated observation, not a certification or vendor ranking.
Attribute presence, rule violations, conditional absence, and unsupported signals
are different findings. The successful inference scenario need not emit `error.type`.
The report's signal classifications do not exhaust all telemetry emitted.
Do not claim Weaver alone proves context propagation or semantic correctness.

## Community adoption: slide 26

- [OpenInference #3024](https://github.com/Arize-ai/openinference/pull/3024): opt-in GenAI attributes alongside existing fields.
- [Donation PR #1](https://github.com/open-telemetry/donation-openinference/pull/1): merged June 16, 2026; this is the date shown on the donation slide.
- [Arize code grant](https://github.com/open-telemetry/community/issues/3467): instrumentation code, not the OpenInference specification.
- [OpenLLMetry LangChain #3673](https://github.com/traceloop/openllmetry/pull/3673).
- [OpenLLMetry Anthropic #3835](https://github.com/traceloop/openllmetry/pull/3835).
- [OpenLLMetry OpenAI #3844](https://github.com/traceloop/openllmetry/pull/3844).
- [OpenLLMetry Gemini #3840](https://github.com/traceloop/openllmetry/pull/3840).
- [Anthropic native tracing commit](https://github.com/anthropics/anthropic-sdk-python/commit/02c93c199b78c3f9bbe59cf424162f8a3868d5ed).
- [Anthropic SDK tracing guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry/sdk).

Adoption means concrete progress with specific scope. It does not mean every
package, attribute, signal, configuration option, or propagation path conforms.

## Attribute examples and inference screenshot

- OTel trace: `b4cb8caea3e1fcb89990608063021e13`, span `5229dc81c79ee457`.
- Source: `opentelemetry.instrumentation.genai.langchain` version `1.3b0`.
- `assets/otel-inference-attributes.json` preserves the exported values. The content slide decodes the message JSON, omits null names, and shows the first of two tool calls.
- `assets/aspire-inference-attributes.png` shows only the first inference span's attributes table.
- `assets/aspire-genai-conversation-long.png` shows the final inference span `6483b37c228ebddd` in the same trace: the question, two tool calls, both tool results, and the final answer. It reports 300 input and 60 output tokens.
- Agent IDs, versions, descriptions, separate instructions, and request-parameter fields are convention coverage, not claims that every demo span emitted them.
- Attribute definitions: `model/gen-ai/registry.yaml`; structured messages and tool definitions: `model/gen-ai/gen-ai-*-messages.json` and `model/gen-ai/gen-ai-tool-definitions.json`.

## OpenAI instrumentation snippet

Simplified from the local Python GenAI checkout at `c96530619b5324e78ffc83c615ef3e6905f1419d`:

- [OpenAI wrapper and response mapping](https://github.com/open-telemetry/opentelemetry-python-genai/blob/c96530619b5324e78ffc83c615ef3e6905f1419d/instrumentation/opentelemetry-instrumentation-genai-openai/src/opentelemetry/instrumentation/genai/openai/patch.py).
- [Inference creation](https://github.com/open-telemetry/opentelemetry-python-genai/blob/c96530619b5324e78ffc83c615ef3e6905f1419d/instrumentation/opentelemetry-instrumentation-genai-openai/src/opentelemetry/instrumentation/genai/openai/utils.py).
- [Streaming lifecycle](https://github.com/open-telemetry/opentelemetry-python-genai/blob/c96530619b5324e78ffc83c615ef3e6905f1419d/instrumentation/opentelemetry-instrumentation-genai-openai/src/opentelemetry/instrumentation/genai/openai/chat_wrappers.py).

The slide inlines selected request and response mappings for a non-streaming call and uses the utility context manager, which calls stop() or fail() on exit. The upstream wrapper uses explicit lifecycle calls to also support streaming. Returning a stream from the context-manager block would end the operation too early.

## Session

- [Official session](https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/program/schedule/?id=1246166): The Race to Standardize AI Observability, November 12, 2026.
- [OpenTelemetry speaker listing](https://opentelemetry.io/blog/2026/kubecon-na/): Liudmila Molkova, Google; Trask Stalnaker, Microsoft.
