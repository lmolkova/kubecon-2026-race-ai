# GenAI instrumentation, adoption, and the 2026 timeline

Research snapshot: November 1, 2026. Read-only review of documentation, source,
merged changes, and committed conformance results. No scenarios or tests run.

Timeline expansion checked November 5, 2026. The earlier Python/JS counts below
retain their November 1 cutoff. Dates in the new tables are UTC merge dates
unless marked as a release announcement. Merged support does not establish
which published package first shipped it.

## 2026 timeline beyond Python and JavaScript

Use these milestones for slide 17 and its future continuation. The scope is
AI observability across OTel.
This is a selected milestone inventory, not every OTel change in 2026.

### Java: existing clients gain depth, new frameworks gain coverage

| Date | Milestone and evidence | Scope for the talk |
| --- | --- | --- |
| January 5 | [Bedrock inference-profile model IDs, #15751](https://github.com/open-telemetry/opentelemetry-java-instrumentation/pull/15751) | Support regional/global model-ID prefixes. Included in [v2.24.0](https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/tag/v2.24.0), published January 17. This improves existing Bedrock instrumentation. |
| June 9 | [GenAI exception logs, #18893](https://github.com/open-telemetry/opentelemetry-java-instrumentation/pull/18893) | OpenAI failures can emit exception logs under the preview opt-in. Included in [v2.29.0](https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/tag/v2.29.0), published June 19. |
| October 3, release | [Java instrumentation v2.32.0](https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/tag/v2.32.0) | Streaming-request attributes, OpenAI cached/reasoning token counts, and Bedrock guardrail IDs. These add detail to existing instrumentation. |
| October 16 | [Spring AI ChatModel, #19473](https://github.com/open-telemetry/opentelemetry-java-instrumentation/pull/19473), `lrwh` | New Java agent instrumentation for Spring AI 1.x, including synchronous and streaming calls, client spans, and metrics. Captures the provider-neutral ChatModel interface. Message content is opt-in. |
| November 4 | [MCP Java SDK, #20062](https://github.com/open-telemetry/opentelemetry-java-instrumentation/pull/20062), `walleseve` | New client instrumentation for SDK 0.14.1+, synchronous/asynchronous tool calls, duration metrics, and context propagation. Tool arguments/results are outside this PR's capture scope. |
| November 4 | [OpenAI Responses API, #20537](https://github.com/open-telemetry/opentelemetry-java-instrumentation/pull/20537), `sangkyoonnam` | Adds spans and metrics for sync/async and streaming Responses calls. Content capture is deferred. This extends the existing OpenAI integration. |

Do not call all six rows new instrumentations. Spring AI and MCP are new
integration coverage; the other rows improve existing clients. November merges
are newer than the original research snapshot and should be labeled merged
until a containing release is verified.

### Go compile-time instrumentation: GenAI coverage arrives in 2026

| Date | Milestone and evidence | Scope for the talk |
| --- | --- | --- |
| July 2 | [OpenAI Go SDK, #604](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/pull/604), `NameHaibinZhang` | New support for SDK v1/v2/v3: chat, text completions, embeddings, and streaming. Three SDK majors are one library integration, not three independent instrumentations. |
| July 19 | [Anthropic Go SDK, #689](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/pull/689), `pradhyum6144` | New non-streaming Messages API instrumentation. Streaming and content capture were deferred in this initial change. |
| July 31 | [Anthropic duration metric, #775](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/pull/775), `malladinagarjuna2` | Adds the operation-duration histogram, including failed calls. |
| September 2 | [OpenAI duration metric and Anthropic error dimensions, #1074](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/pull/1074), `Labreo` | Adds OpenAI operation-duration metrics and error classification on Anthropic duration metrics. |
| September 7 | [OpenAI opt-in content capture, #740](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/pull/740), `Aryanbhargava18` | Adds bounded prompt/completion capture. Embedding content is excluded. |
| October 28 | [Avoid duplicate Anthropic spans, #1572](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/pull/1572), `amazingakai` | Handles coexistence with native SDK OpenTelemetry. Useful evidence that native and external instrumentation must compose. |

The timeline shows depth arriving after initial span coverage: metrics, content
controls, and coexistence fixes.

### OBI/eBPF: model calls, tools, and retrieval

| Date | Milestone and evidence | Author |
| --- | --- | --- |
| February 25 | [OpenAI protocol support, #1353](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/1353) | `grcevski` |
| March 31 | [GenAI metrics, #1672](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/1672) | `grcevski` |
| April 23 and 27 | [Qwen, #1892](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/1892) and [MCP, #1867](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/1867) | `NameHaibinZhang` |
| May 8 and 13 | [Reranking, #2056](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/2056) and [vector retrieval, #2087](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/2087) | `NameHaibinZhang` |
| July 22 | [Native Ollama chat/generate endpoints, #2710](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/2710) | `NameHaibinZhang` |
| October 14 | [GenAI upstream conformance, #3707](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/3707) | `NimrodAvni78` |
| October 26 | [Cohere v2 chat, #3903](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/3903) | `nirajan1111` |
| November 4 | [Ollama embedding spans, #4014](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/4014) | `DCchoudhury15` |

OBI observes supported protocols and payloads across applications. Its coverage
units differ from Python package or Go SDK counts. Do not add them into a single
"number of instrumentations" total.

The [v1 announcement](https://opentelemetry.io/blog/2026/obi-v1-release/) ties the
release to configuration/deployment compatibility and telemetry migration
guidance, including a Weaver-compatible registry. GenAI extraction needs explicit
payload-capture and feature configuration. The release does not make all emitted
telemetry stable or give visibility into arbitrary internal agent steps.

### Work across OTel and coordination with AAIF

| Date | Milestone and evidence | Why it belongs on the timeline |
| --- | --- | --- |
| May 5 | [GenAI conventions move to their own repo, #3696](https://github.com/open-telemetry/semantic-conventions/pull/3696) | A dedicated place for the domain's conventions and reference scenarios. |
| May 12 and 22 | Collector [OpenInference normalization, #48245](https://github.com/open-telemetry/opentelemetry-collector-contrib/pull/48245) and [OpenLLMetry mapping, #48385](https://github.com/open-telemetry/opentelemetry-collector-contrib/pull/48385) | Migration help for existing span attributes. These changes do not establish normalization of logs, metrics, or missing context. |
| May 13, charter approval field | [AAIF Observability & Traceability charter](https://github.com/aaif/wg-observability-and-traceability/blob/main/charter/CHARTER.md) | A coordination forum connecting existing efforts, including OTel GenAI. The charter records WG ratification on April 15 and approval on May 13, but its final ratification block still has placeholders. Label this as the charter's recorded date, not a verified launch announcement. |
| May 19 | [Memory operation conventions, #140](https://github.com/open-telemetry/semantic-conventions-genai/pull/140) | Coverage expands to memory-store and memory-record operations, grounded in framework reference scenarios. Merged conventions are not a stability declaration. |
| June 1 | [Collector GenAI normalizer promoted to alpha, #48773](https://github.com/open-telemetry/opentelemetry-collector-contrib/pull/48773) | Added to the contrib distribution configuration. Implementation followed the May scaffold; cite this milestone rather than treating the scaffold as working support. |
| August 8 | [Conformance runner and GenAI domain, #12](https://github.com/open-telemetry/semantic-conventions-conformance/pull/12) | Shared runner, Weaver validation, and a deterministic provider mock server. This PR adds tooling; scenarios follow separately. |
| October 26 | [Content capture/upload configuration, #543](https://github.com/open-telemetry/semantic-conventions-genai/pull/543) | Formalizes shared configuration. Existing implementations still need adoption checks. |
| November 4 | [Realtime session conventions, #394](https://github.com/open-telemetry/semantic-conventions-genai/pull/394) | Adds realtime inference, speech, session correlation, and audio/transcription modeling with OpenAI Realtime and Gemini Live reference scenarios. |

AAIF is an external collaboration milestone, not an OTel subproject. Its
[README](https://github.com/aaif/wg-observability-and-traceability) dates the chairs'
term from March 1, 2026; that is not evidence of the group's exact launch date.

### Contributor evidence beyond Python/JS

Two verified examples of first public merged OTel PRs:

| Account | First merged PR | Merge timestamp, UTC |
| --- | --- | --- |
| `malladinagarjuna2` | [Go Anthropic duration metrics, #775](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/pull/775) | 2026-07-31T04:15:11Z |
| `nirajan1111` | [OBI Cohere chat, #3903](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/3903) | 2026-10-26T21:29:58Z |

Checked November 5 using the same public merged-PR definition as the Python/JS
research. Each query returned zero earlier matches:

```text
org:open-telemetry is:pr is:merged author:malladinagarjuna2 merged:<2026-07-31T04:15:11Z
org:open-telemetry is:pr is:merged author:nirajan1111 merged:<2026-10-26T21:29:58Z
```

These are examples, not an exhaustive newcomer count. Checks for `lrwh`,
`walleseve`, `sangkyoonnam`, `pradhyum6144`, and `DCchoudhury15` found earlier
OTel merges. In particular, `walleseve` and `sangkyoonnam` also contributed in
Python GenAI, so adding per-repo author counts would double-count them.

### Suggested timeline selection

Stabilization milestone checked November 5: [inference and core agentic execution stabilization, #511](https://github.com/open-telemetry/semantic-conventions-genai/issues/511) was opened September 11, 2026. Use September for the start of the tracked stabilization effort, not a declaration of stability. The issue defines scope across spans, metrics, and events; some operations remain undecided.

For one slide, select milestones rather than reproducing the inventory:
February OBI OpenAI support; May dedicated GenAI conventions and AAIF coordination;
July Python beta delivery and Go GenAI coverage; August conformance tooling;
October Spring AI, OBI GenAI conformance, and shared content configuration; November Java MCP
and Responses support. Use the Python/JS sections below for their exact dates.

Keep future RC targets and 2027 breadth on a separate continuation. Completed
coverage already includes memory, MCP, retrieval, and realtime conventions;
frame future work as stabilization, deeper implementation, and remaining gaps
rather than implying those areas have no work today.

## Claims we can use in the talk

| Project | Evidence | Precise claim |
| --- | --- | --- |
| OpenInference | [PR #3024](https://github.com/Arize-ai/openinference/pull/3024), merged May 14, 2026 | Python's shared tracer gained opt-in OTel GenAI attribute emission alongside existing OpenInference attributes. Default behavior was unchanged by this change. |
| OpenLLMetry | [LangChain #3673](https://github.com/traceloop/openllmetry/pull/3673), March 3; [Anthropic #3835](https://github.com/traceloop/openllmetry/pull/3835) and [OpenAI #3844](https://github.com/traceloop/openllmetry/pull/3844), March 29; [Gemini #3840](https://github.com/traceloop/openllmetry/pull/3840), April 9, 2026 | Multiple instrumentations migrated toward OTel GenAI conventions. This was package-by-package adoption, not proof that every package implements every convention. |
| Anthropic Python SDK | [Native tracing commit](https://github.com/anthropics/anthropic-sdk-python/commit/02c93c199b78c3f9bbe59cf424162f8a3868d5ed), October 14, 2026; [SDK guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry/sdk) | The SDK emits native OTel spans through the application's tracer provider and uses its propagator. It records GenAI attributes, with remaining differences visible in conformance results. |
| Mistral Python SDK | [PR #280](https://github.com/mistralai/client-python/pull/280), merged December 2, 2025 | Native tracing explicitly targeted OTel GenAI conventions. It is a credible candidate for the early-2026 demo. |

For OpenInference, the concrete switch introduced was
`OPENINFERENCE_ENABLE_GENAI_SEMCONV` / `TraceConfig.enable_genai_semconv`.
The mapping uses the final masked OpenInference attributes and preserves explicit
caller-provided GenAI attributes. This is schema adoption, not evidence that it
adds metrics, common configuration, or every missing field.

OpenLLMetry's OpenAI change also introduced structured input/output messages
behind `use_messages_attributes`. Pin configuration as well as package versions
when comparing old and new telemetry.

Arize's [code grant](https://github.com/open-telemetry/community/issues/3467) is a
separate contribution: it donates instrumentation code for OTel to adapt.
It explicitly excludes the OpenInference specification and does not transfer
the OpenInference project or require specification convergence. Celebrate both
contributions without conflating them.

## Native instrumentation already affects OTel's maintenance decisions

[Python GenAI issue #141](https://github.com/open-telemetry/opentelemetry-python-genai/issues/141)
marks Pydantic AI, Google ADK, Mistral, and MCP as “won't port” because native
instrumentation exists. It also points to native instrumentation for LiteLLM,
LlamaIndex, Haystack, AutoGen, BeeAI, Strands, Microsoft Agent Framework, and
Pipecat. These entries have different statuses; “native” does not mean fully
conformant.

The [contribution policy](https://github.com/open-telemetry/opentelemetry-python-genai/blob/main/CONTRIBUTING.md#when-to-add-an-instrumentation-here)
encourages native instrumentation or first-party plugins. For reasonably
compatible implementations, it says to record gaps and work with the authors
rather than duplicate instrumentation. It also calls for reconsidering existing
OTel packages when compatible first-party instrumentation arrives.

Suggested line:

> We want telemetry maintained close to the library. Our goal is a comparable
> experience wherever the instrumentation comes from.

## What the conformance repo actually measures

The [dashboard](https://open-telemetry.github.io/semantic-conventions-conformance/)
and [stored report](https://github.com/open-telemetry/semantic-conventions-conformance/blob/5ff0737b53f922b4a0006cd17577c10512f30a32/docs/data/conformance.json)
compare instrumentations against a registry and scenario set.

The [scenario documentation](https://github.com/open-telemetry/semantic-conventions-conformance/blob/5ff0737b53f922b4a0006cd17577c10512f30a32/scenarios/gen-ai/README.md)
defines native as built-in instrumentation or first-party plugins. Implementations
of the same client share scenario programs; each implementation has an isolated
environment. The current scenarios run in report-only mode without scenario
expectations. They measure emitted telemetry and record findings rather than
certifying completeness or failing the build on every finding.

Native Python targets present in this snapshot:

| Library | Registry-classified signals in the stored results |
| --- | --- |
| Anthropic | Inference, tool execution, agent invocation spans |
| Mistral | Inference and embeddings spans |
| Pydantic AI | Inference, tool execution, agent invocation spans |
| Google ADK | Inference, tool, agent, workflow spans; inference details event; several operation metrics |
| Microsoft Agent Framework | Inference, tool, agent spans; operation-duration metric |
| AutoGen | Agent creation, tool, client agent-invocation spans |
| Strands Agents | Inference, tool, agent spans |
| LiteLLM | Inference and embeddings spans; operation-duration and token-timing metrics |
| Haystack, LlamaIndex | Native targets exist, but no signals were classified into the report's registry signal list |

These are classified results, not an exhaustive inventory of emitted telemetry.
For example, Pydantic AI's findings include an emitted token-usage metric that
the selected registry does not recognize. An empty metric list cannot establish
that the library emits no metrics. Findings can also reflect custom extensions
or convention-version differences.

## Concrete examples for the dialogue

### Native integration can improve application-owned configuration

Mistral's [January 6, 2026 change](https://github.com/mistralai/client-python/commit/99cae3ab336536d98b981ca615d5b9fbf6502113)
removed SDK setup of its own tracer provider/exporter and relied on application
configuration. It also changed outgoing context injection to use the request
span explicitly.

This supports the “configure once” wish with a real improvement. The original
native tracing existed before 2026, correcting our earlier uncertainty. Still
verify the selected released package and mixed-trace behavior before the demo.

### Shared attributes can coexist with different span names

The [Anthropic native report](https://github.com/open-telemetry/semantic-conventions-conformance/blob/5ff0737b53f922b4a0006cd17577c10512f30a32/scenarios/gen-ai/python/anthropic/native/data.json)
identifies these naming differences:

| Emitted name | Expected by the report's convention |
| --- | --- |
| `anthropic.messages.create` | `chat {model}` |
| `anthropic.custom_tool_use get_current_weather` | `execute_tool get_current_weather` |
| `anthropic.messages.tool_runner` | `invoke_agent` |

This is an understandable drill-down for the dashboard demonstration: native
OTel integration and GenAI attributes are useful progress, while the report
makes remaining differences visible. Do not equate every finding with a defect;
confirm the applicable registry version, requirement level, and provider-specific
conventions before making a remediation claim.

### Content configuration still differs

- [Anthropic](https://github.com/open-telemetry/semantic-conventions-conformance/blob/5ff0737b53f922b4a0006cd17577c10512f30a32/scenarios/gen-ai/python/anthropic/native/conformance.yaml):
  `ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE=content`. Its SDK documentation
  describes metadata-only capture by default.
- [Pydantic AI](https://github.com/open-telemetry/semantic-conventions-conformance/blob/5ff0737b53f922b4a0006cd17577c10512f30a32/scenarios/gen-ai/python/pydantic-ai/native/conformance.yaml):
  the scenario notes content is recorded by default and controlled through a
  constructor argument.
- [OTel instrumentations](https://github.com/open-telemetry/semantic-conventions-conformance/blob/5ff0737b53f922b4a0006cd17577c10512f30a32/scenarios/gen-ai/README.md#content-capture):
  the scenario documentation uses
  `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`.

This is evidence for the common-content-policy wish. It does not establish
that sanitization or external upload hooks are equivalent across implementations.

## How to present the feedback loop

Show one reproducible scenario, the emitted span, the relevant convention, and
the dashboard finding. Give the maintainer an actionable compatibility report.
Avoid inferring a maintainer's OTel expertise or intentions from a mismatch.

Weaver Live Check is part of the mechanism; the harness also supplies registry
pins, domain policies, collection, and aggregation. The repository already
contains HTTP and database domains, supporting the claim that this approach
extends beyond GenAI.

Use the findings to motivate collaboration, not a vendor ranking. Coverage
depends on exercised scenarios, configuration, SDK versions, and registry version.

## Remaining preparation

### Python GenAI delivery numbers

As of November 1, 2026, the [GitHub releases](https://github.com/open-telemetry/opentelemetry-python-genai/releases)
show four coordinated beta release rounds: 1.0b0 on July 9, 1.1b0 on August 20,
1.2b0 on September 24, and 1.3b0 on October 23. Additional package patches were
published as 1.0b1 and 1.1b1. Count rounds rather than individual package release
entries when saying how often the project released.

The [released-instrumentation table](https://github.com/open-telemetry/opentelemetry-python-genai#released-instrumentations)
lists 13 packages: Agno, Anthropic, Bedrock, DSPy, LangChain, LlamaIndex, OpenAI,
OpenAI Agents, Portkey, Qwen Agent, QwenPaw, Smolagents, and Google GenAI.
The first release round contained five instrumentation packages, so the released
inventory grew by eight. Three additional directories are marked unreleased
skeletons and are excluded from this count. These are package counts, not counts
of fully implemented libraries or certified integrations.

The repo README says all instrumentations use `opentelemetry-util-genai`.
[Migration guidance in #141](https://github.com/open-telemetry/opentelemetry-python-genai/issues/141)
requires shared utilities for consistent telemetry, configuration, and hooks,
and calls for AI-assisted migration/review skills plus conformance tests.

### Before presenting

#### Contributor growth and weekly throughput

Computed November 1, 2026 using GitHub GraphQL's merged pull requests and exact
`mergedAt` timestamps. The repo was created May 12, 2026. At retrieval, it had
358 contributor-authored merged PRs.

There are **47 distinct human PR-author accounts**, of which **24 have no earlier
merged PR found in another public repository in the OpenTelemetry organization**.
This is a first-merged-PR measure, not a claim that these people had never attended
a SIG, reviewed code, opened issues, or contributed elsewhere. Accounts are not
deduplicated into people.

For each author, find their first exact merge timestamp here, then search:

```text
org:open-telemetry -repo:open-telemetry/opentelemetry-python-genai
is:pr is:merged author:LOGIN merged:<FIRST_MERGE_TIMESTAMP
```

Only individual contributor accounts are included. The count relies on public
GitHub search history.

| First-time merged-PR contributor account | First Python GenAI PR | Merge date, UTC |
| --- | --- | --- |
| 1fanwang | [#538](https://github.com/open-telemetry/opentelemetry-python-genai/pull/538) | 2026-09-03 |
| AgentGymLeader | [#111](https://github.com/open-telemetry/opentelemetry-python-genai/pull/111) | 2026-06-18 |
| FeelKyoun | [#522](https://github.com/open-telemetry/opentelemetry-python-genai/pull/522) | 2026-09-20 |
| HQidea | [#358](https://github.com/open-telemetry/opentelemetry-python-genai/pull/358) | 2026-09-14 |
| Pr1meGG | [#861](https://github.com/open-telemetry/opentelemetry-python-genai/pull/861) | 2026-10-11 |
| SAMurai-16 | [#671](https://github.com/open-telemetry/opentelemetry-python-genai/pull/671) | 2026-09-10 |
| Shailendra005 | [#381](https://github.com/open-telemetry/opentelemetry-python-genai/pull/381) | 2026-08-14 |
| Thanatos9404 | [#881](https://github.com/open-telemetry/opentelemetry-python-genai/pull/881) | 2026-10-15 |
| VimalN2005 | [#853](https://github.com/open-telemetry/opentelemetry-python-genai/pull/853) | 2026-10-09 |
| Yigtwxx | [#366](https://github.com/open-telemetry/opentelemetry-python-genai/pull/366) | 2026-08-11 |
| alexander-akhmetov | [#349](https://github.com/open-telemetry/opentelemetry-python-genai/pull/349) | 2026-08-03 |
| alexliluz | [#397](https://github.com/open-telemetry/opentelemetry-python-genai/pull/397) | 2026-08-26 |
| benkawecki | [#781](https://github.com/open-telemetry/opentelemetry-python-genai/pull/781) | 2026-10-21 |
| bhumikadangayach | [#153](https://github.com/open-telemetry/opentelemetry-python-genai/pull/153) | 2026-06-23 |
| bhushanasati25 | [#656](https://github.com/open-telemetry/opentelemetry-python-genai/pull/656) | 2026-09-10 |
| dlowzzxx | [#633](https://github.com/open-telemetry/opentelemetry-python-genai/pull/633) | 2026-09-10 |
| girishkvs | [#793](https://github.com/open-telemetry/opentelemetry-python-genai/pull/793) | 2026-10-02 |
| jaeminbird | [#1017](https://github.com/open-telemetry/opentelemetry-python-genai/pull/1017) | 2026-10-31 |
| ordemri | [#485](https://github.com/open-telemetry/opentelemetry-python-genai/pull/485) | 2026-08-29 |
| pcbeingused333 | [#908](https://github.com/open-telemetry/opentelemetry-python-genai/pull/908) | 2026-10-20 |
| pylaterreur | [#819](https://github.com/open-telemetry/opentelemetry-python-genai/pull/819) | 2026-10-01 |
| samtin0x | [#992](https://github.com/open-telemetry/opentelemetry-python-genai/pull/992) | 2026-10-28 |
| somuai | [#913](https://github.com/open-telemetry/opentelemetry-python-genai/pull/913) | 2026-10-22 |
| venkata-pavani | [#308](https://github.com/open-telemetry/opentelemetry-python-genai/pull/308) | 2026-08-04 |

Weekly throughput covers the repo's full history from creation on May 12 through
the November 1 snapshot. Weeks are Monday-Sunday in America/Los_Angeles. The
creation week and current week are included and marked partial; the average
uses all 23 complete weeks, May 18-October 25.

| Week starting | Contributor-authored merged PRs |
| --- | ---: |
| 2026-05-11 (partial) | 4 |
| 2026-05-18 | 17 |
| 2026-05-25 | 1 |
| 2026-06-01 | 4 |
| 2026-06-08 | 7 |
| 2026-06-15 | 11 |
| 2026-06-22 | 6 |
| 2026-06-29 | 3 |
| 2026-07-06 | 28 |
| 2026-07-13 | 12 |
| 2026-07-20 | 8 |
| 2026-07-27 | 14 |
| 2026-08-03 | 8 |
| 2026-08-10 | 6 |
| 2026-08-17 | 19 |
| 2026-08-24 | 14 |
| 2026-08-31 | 40 |
| 2026-09-07 | 34 |
| 2026-09-14 | 24 |
| 2026-09-21 | 13 |
| 2026-09-28 | 13 |
| 2026-10-05 | 18 |
| 2026-10-12 | 13 |
| 2026-10-19 | 26 |
| 2026-10-26 (partial) | 15 |
| Total since creation | 358 |
| Complete-week total | 339 |
| Complete-week average | 14.74 |

Suggested slide wording: **“24 first-time OTel merged-PR contributors in Python
GenAI; about 15 contributor-authored PRs merged per week since launch.”**
Put the definition and date window in
speaker notes. These counts cover all PR types, not just new instrumentations.

Source: [Python GenAI merged PRs](https://github.com/open-telemetry/opentelemetry-python-genai/pulls?q=is%3Apr+is%3Amerged).
The per-person links above make the first merges inspectable; rerun the same
queries before presenting.

#### JavaScript follows the approach

[JS migration issue #3668](https://github.com/open-telemetry/opentelemetry-js-contrib/issues/3668)
tracks 11 candidate packages from the OpenInference donation. It explicitly
references Python's shared utility approach, conformance tests, and AI-assisted
migration/review skills. Unlike Python, the target is the existing
`opentelemetry-js-contrib` monorepo.

Describe this as work in progress, not 11 completed ports. The tracker also
calls for checking native instrumentation and reconciling existing packages
rather than duplicating them.

#### JavaScript AI-related merged PRs

Scope: January 1-November 1, 2026, in `opentelemetry-js-contrib`. Include
AI instrumentation, GenAI utilities, AI-specific ownership, and OpenInference
migration skills. Include #3828 because it explicitly updates LangChain tests
alongside other components; exclude general repository-wide maintenance from
the AI count. This is a broader AI-work inventory, not solely donation ports.

Reviewed the year's contributor-authored merged PR titles, searched across AI
package names, and checked candidate PR files and exact merge timestamps.
The scoped list contains **15 PRs from eight authors**.

| PR | Merged, UTC | Author | Change | First merged OTel PR? |
| --- | --- | --- | --- | --- |
| [#3132](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3132) | 2026-03-11 | yiyuan-he | feat(instrumentation-langchain): add initial package skeleton for instrumentation-langchain | No |
| [#3446](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3446) | 2026-03-19 | hectorhdzg | chore: Adding hectorhdzg as component owner for GenAI instrumentations | No |
| [#3555](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3555) | 2026-06-10 | micael-mbagira-parloa | fix(instrumentation-openai): guard stream iterator against chunks missing a choices array | Yes |
| [#3194](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3194) | 2026-07-01 | btomaj | feat(instrumentation-openai): support Responses API | Yes |
| [#3671](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3671) | 2026-08-27 | JacksonWeber | docs: add OpenInference migration skill | No |
| [#3709](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3709) | 2026-09-10 | psx95 | feat(genai-util): scaffold package, types, semconv and core utils | No |
| [#3712](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3712) | 2026-09-14 | psx95 | feat(genai-util): add GenAI metric helpers and histograms | No |
| [#3757](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3757) | 2026-09-21 | psx95 | feat(genai-util): add base invocation lifecycle and TelemetryHandler | No |
| [#3772](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3772) | 2026-09-30 | psx95 | feat(genai-util): accept structured InvocationError in fail() | No |
| [#3774](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3774) | 2026-10-12 | JacksonWeber | feat(instrumentation-langchain): trace composed workflow invocations | No |
| [#3762](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3762) | 2026-10-13 | psx95 | feat(genai-util): add support for core invocations | No |
| [#3828](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3828) | 2026-10-14 | overbalance | chore(contrib-test-utils, instrumentation-langchain, instrumentation-runtime-node): replace APIs removed in OpenTelemetry JS 3.x | No |
| [#3851](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3851) | 2026-10-21 | overbalance | docs: restore the OpenInference migration skill and update it for tsdown | No |
| [#3699](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3699) | 2026-10-22 | eternalcuriouslearner | feat(instrumentation-openai-agents): add instrumentation | No |
| [#3821](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3821) | 2026-10-29 | JacksonWeber | feat(instrumentation-langchain): migrate donated tool execution | No |

**Two additional newcomers:** `btomaj` and `micael-mbagira-parloa`. For each
author, searched all public OTel repositories for merged PRs before their first
AI-related JS merge, including earlier non-AI PRs in JS contrib. Use:

```text
org:open-telemetry is:pr is:merged author:LOGIN merged:<FIRST_AI_JS_MERGE_TIMESTAMP
```

The other six authors already had merged OTel contributions. JacksonWeber and
eternalcuriouslearner also appear among Python GenAI contributors, so deduplicate
across repos: **53 distinct contributor accounts and 26 first-time merged-PR
contributors across Python GenAI and this JS AI scope**.

This does not imply all JS AI contributors were new to JS contrib, or that the
newcomers' PRs were produced through the donation workflow.

#### Outstanding checks

- Pin released versions for the early-2026 mixed-schema demo; keep later
  adoption milestones in the “what changed in 2026” section.
- Verify both directions of LangSmith context propagation before including it
  in a connected trace.
- Confirm the chosen release's OpenInference opt-in and OpenLLMetry message
  settings. Merged changes establish dates, not installation defaults forever.
- Gather a public upstream issue or merged fix driven by conformance findings
  if we want to show the feedback loop completed. This research establishes
  the policy and actionable findings, not that a particular finding caused a fix.
- Source the first stabilization wave separately; it was outside this native
  instrumentation/adoption pass.
