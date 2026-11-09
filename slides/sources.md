# Sources and notes

## OpenTelemetry mission: slide 2

- [Mission, vision, and values](https://github.com/open-telemetry/community/blob/main/mission-vision-values.md#mission), quoted verbatim with the first letter capitalized.

## Demo evidence: slides 3, 5-10, 13

- Code: [demo](../demos/kubecon-genai/demo.py), [locked versions](../demos/kubecon-genai/uv.lock).
- Main trace: `b2fb5dc7fc85244d41a7f3667beaec03`.
- Orphan trace: `01a1a3cdcf8a74568f6fdd9c7c86e09f`, HTTP span `f88b071f40ee83f4`.
- OpenTelemetry instrumentations trace: `36834b4c2a254ac26e29cecc1976d634`, from [compose.otel.yaml](../demos/kubecon-genai/compose.otel.yaml), 16 spans.
- Two application services; local mocks; four successful model requests.
- Model IDs: `gpt-4.1`, `claude-sonnet-4-6`, and `gpt-4.1-mini`.
- Original Aspire screenshots recaptured in light mode on November 3, 2026; the full waterfall and separate orphan HTTP capture are retained in `assets/aspire-waterfall.png` and `assets/aspire-orphan-http.png`.
- Slide 5 is a collapsed vector redraw of the saved main-trace capture, keeping displayed names, resources, nesting, and markers. It expands the first model call and the inspect_workload tool and hides the three root-level model HTTP spans and the separate orphan span. Original displayed durations are retained in SVG metadata, not a visible column. Bar shapes are traced from screenshot pixels; no exact start/end timestamps were recovered. Its three click steps box the expanded subtrees, the empty consult_runbook tool, and the detached runbook subtree, with an arrow to the intended parent; they do not change the captured hierarchy.
- The three trace images on slides 5, 6, and 12 omit image titles, capture summaries, and footer captions. Provenance and interpretation remain in these notes and the SVG accessibility descriptions.
- Slide 6's span names and nesting follow the OpenTelemetry instrumentations trace. Chat spans are collapsed, hiding the HTTP client span under each, like slide 5 hides its model HTTP spans; only the runbook call's HTTP client span is expanded. Its 12 bars follow the matching spans on slide 5's 0–0.7 s axis. These are screenshot positions, not recovered OTLP timestamps; the SVG metadata records the mapping, hidden children, and instrumentation scopes.
- Slide 12's operation-coverage diagram retains illustrative timing and nesting; it is not a measured demo trace.
- Slide 6 uses slide 5's layout, with the service column moved right to fit the longer names. HTTP client spans on slides 5 and 6 are labeled `POST 200`, Aspire's `HTTP POST 200` label without the prefix. The span hidden under `chat claude-sonnet-4-6` is the Anthropic SDK's native `anthropic.messages.create` span. Blue identifies diagnostic-agent and amber identifies runbook.
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
- HTTPX is enabled in runbook. Its outgoing HTTP span is exported in the separate trace above with an unexported parent; the lower red arrow marks the intended ChatOpenAI parent.
- HTTP metrics and ordinary application logs are not evidence of GenAI signal parity.
- Slide 8 is an illustrative cost chart, not captured telemetry or billing. Both series use USD by usage date; provider data has an invented one-day delay. The demo's 60% missing input tokens does not imply 60% missing cost.
- Slide 9's [instrumentation diagram](assets/instrumentation-architecture.svg) shows application calls and instrumentation sources, not measured span parentage.
- Slide 3's [application diagram](assets/application-architecture.svg) uses the same layout without instrumentation sources.

## Project timeline: slide 17

The eight milestones use the [2026 research inventory](../kubecon-talk-research.md#2026-timeline-beyond-python-and-javascript) and its Python/JavaScript sections. Stops are evenly spaced, not a calendar scale.

- February: OBI OpenAI protocol support, merged February 25.
- March: OpenLLMetry GenAI conventions for [LangChain #3673](https://github.com/traceloop/openllmetry/pull/3673) (March 3), [Anthropic #3835](https://github.com/traceloop/openllmetry/pull/3835) and [OpenAI #3844](https://github.com/traceloop/openllmetry/pull/3844) (March 29); [Gemini #3840](https://github.com/traceloop/openllmetry/pull/3840) followed April 9.
- May: dedicated GenAI conventions repository and Python GenAI repository.
- June: one stop for two OpenInference contributions. [OpenInference #3024](https://github.com/Arize-ai/openinference/pull/3024), merged May 14, adds opt-in GenAI conventions export alongside existing OpenInference attributes. The [Arize code grant](https://github.com/open-telemetry/community/issues/3467) was proposed May 23 and accepted June 16; [donation PR #1](https://github.com/open-telemetry/donation-openinference/pull/1) merged June 16. The grant covers instrumentation code, not the OpenInference specification. OpenInference remains a separate project.
- July: first Python beta on July 9; Go OpenAI and Anthropic support merged July 2 and 19 in [opentelemetry-go-compile-instrumentation](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation).
- August: conformance runner and GenAI domain merged August 8.
- September: [inference and core agentic execution stabilization tracking issue](https://github.com/open-telemetry/semantic-conventions-genai/issues/511) opened September 11. This marks the tracked stabilization effort, not stable conventions.
- October-November: native Anthropic Python tracing, Java Spring AI and MCP, and JavaScript OpenAI Agents. Java November entries are merged changes, not verified package releases.

## Conventions and development: slides 11-16, 19-21

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
Four coordinated Python beta release rounds plus patches; 13 released packages, all released in 2026 (PyPI, checked November 7). 12 had their first PyPI release in 2026 under the `genai-` names (July 9 - October 23); Google GenAI first shipped from python-contrib in February 2025. OpenAI and OpenAI Agents previously shipped from contrib as `-v2` packages.
The monthly PR chart counts non-bot merged PRs per UTC month, November 2024
through October 2026, as of November 4, 2026. In `opentelemetry-python-contrib`,
a PR counts when at least half of its changed package-directory files are under
`instrumentation-genai/` or `util/opentelemetry-util-genai/`. Every non-bot PR in
`opentelemetry-python-genai` counts. Bots are GitHub Bot accounts, `[bot]` logins,
and `opentelemetrybot`. Some GenAI packages still live in contrib, so both repos
contribute after May 2026.
Refresh counts before presenting. They are not live dashboard values.

OTel AI contributors (slide 21), checked November 7, 2026: non-bot PRs merged
since January 1, 2026. "New" = no merged PR anywhere in the open-telemetry org
before the author's first AI PR; each newcomer counted once, in the repo of that
first PR. Contributors are deduplicated across repos in the total.

| Repo | Scope | PRs | Contributors | New |
| --- | --- | ---: | ---: | ---: |
| python-genai | all PRs | 371 | 50 | 26 |
| semantic-conventions-genai | all PRs | 204 | 42 | 18 |
| semantic-conventions-conformance | PRs changing gen-ai paths | 62 | 8 | 1 |
| python-contrib | AI keywords in title | 76 | 29 | 10 |
| js-contrib | AI keywords in title | 17 | 8 | 2 |
| java-instrumentation | AI keywords in title | 20 | 9 | 2 |
| go-compile-instrumentation | AI keywords in title | 32 | 19 | 5 |
| ebpf-instrumentation | AI keywords in title | 44 | 10 | 1 |
| ruby-contrib | AI keywords in title | 8 | 5 | 0 |
| **Total** | | **834** | **143** | **65** |

Keywords: genai, gen_ai, "gen ai", openai, anthropic, bedrock, llm, mcp,
"spring ai", ollama, gemini, cohere, qwen, langchain, openinference. Title
matching misses AI PRs without these words, so keyword-scoped repos are
undercounts. Two authors could not be checked (search 422) and count as not new.
.NET excluded.

## Native instrumentation: slide 22

Each library emits OTel itself, using GenAI conventions. Checked November 7, 2026.
- [Anthropic SDK tracing guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry/sdk); [native tracing commit](https://github.com/anthropics/anthropic-sdk-python/commit/02c93c199b78c3f9bbe59cf424162f8a3868d5ed).
- [MCP Python SDK OpenTelemetry docs](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/run/opentelemetry.md): server spans per request, W3C context in `params._meta`. The TypeScript SDK has similar support.
- [Microsoft Agent Framework observability](https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-observability): .NET and Python, `gen_ai.*` spans and metrics, opt-in content.
- [Strands Agents traces](https://strandsagents.com/latest/documentation/docs/user-guide/observability-evaluation/traces/): `invoke_agent`, `chat`, `execute_tool` spans; older or newer convention versions are selectable.
- [Google ADK observability](https://adk.dev/observability/): `invoke_agent` root spans, model and tool child spans.
- [Vercel AI SDK telemetry](https://ai-sdk.dev/docs/ai-sdk-core/telemetry): the `@ai-sdk/otel` integration emits `gen_ai.*`; the `LegacyOpenTelemetry` option keeps the old `ai.*` attributes.

Convention versions and coverage vary by library. Native does not mean conformant.
Logos: [Simple Icons](https://simpleicons.org/) (CC0); trademarks belong to their owners.

## Roadmap: slide 28

The roadmap is direction, not a delivery commitment.
- Targets: release candidate by end of 2026; stable inference, agents/workflows, and tools by KubeCon EU, March 2027. Say "target", not "date".
- Feature by feature: retrievals & embeddings, MCP, and live/realtime are likely next stabilization candidates, not a committed order. Depth work on existing areas continues alongside.
- Longer term: AAIF alignment, agentic identity & security, evaluations, guardrails, harnesses, and trajectories are broad open areas without defined scope. The [AAIF Observability & Traceability charter](https://github.com/aaif/wg-observability-and-traceability/blob/main/charter/CHARTER.md) records approval on May 13, 2026. That is the charter's recorded date, not a verified working-group launch.
Do not imply that planning, arbitrary steps, or every signal has stable coverage.

## Conformance: slides 24-27

- [Comparison report](https://open-telemetry.github.io/semantic-conventions-conformance/#/signals/span%3Agen_ai.client.inference?q=anthropic&level=scored): `gen_ai.client.inference`, filtered to Anthropic, Required + recommended.
- [Native Anthropic report](https://open-telemetry.github.io/semantic-conventions-conformance/#/target/gen-ai/python/anthropic/native).
- [Conformance repository](https://github.com/open-telemetry/semantic-conventions-conformance).
- [Weaver](https://github.com/open-telemetry/weaver).

Screenshots were captured for this deck on November 1, 2026, client local date.
Slide 26's table copies five rows from the comparison report as read on
November 5, 2026. Re-check it before presenting.
The live dashboard identifies GenAI registry revision `9ffc7e00c639`.
This differs from the earlier pinned report in the research document.
Use the screenshots as a dated observation, not a certification or vendor ranking.
Attribute presence, rule violations, conditional absence, and unsupported signals
are different findings. The successful inference scenario need not emit `error.type`.
The report's signal classifications do not exhaust all telemetry emitted.
Do not claim Weaver alone proves context propagation or semantic correctness.

## Attribute examples and inference screenshot

- OTel trace: `b4cb8caea3e1fcb89990608063021e13`, span `5229dc81c79ee457`.
- Source: `opentelemetry.instrumentation.genai.langchain` version `1.3b0`.
- `assets/otel-inference-attributes.json` preserves the exported values. The content slide decodes the message JSON, omits null names, and shows the first of two tool calls.
- `assets/aspire-inference-attributes.png` shows only the first inference span's attributes table.
- The slide 13 attributes table copies that span's `gen_ai.*` values from `assets/otel-inference-attributes.json`. Message and tool-definition values are shortened to the first part, tool call, or tool and omit null names. The chat span has no agent identity attributes, so the top `gen_ai.agent.name` row comes from the `invoke_agent diagnostic` span instead. Its value is the `name="diagnostic"` passed to `create_agent` in `demos/kubecon-genai/demo.py`.
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
