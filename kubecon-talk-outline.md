# We enabled OpenTelemetry. Where is our AI dashboard?

30 minutes, two speakers. Audience: application and platform teams outside the
OTel community.

## 1. We finished instrumentation. Can you help with dashboards? (5 min)

Liudmila shows the application, instrumentation dependencies, configuration, and
readiness report. Everything is checked except dashboards and validation.

One request produces one trace:

```text
Agent                                      Langfuse
├── OpenAI: choose tool                    OpenInference
├── Tool: inspect workload                 Langfuse
│   └── Azure AI Inference: summarize logs OTel GenAI
├── Tool: consult runbook                  Langfuse
│   └── LangChain runbook service          LangSmith OTLP export
│       └── Model: recommend remediation   LangSmith OTLP export
└── OpenAI: explain findings               OpenInference
```

The proposed runbook service belongs to another team and uses LangSmith tracing
exported over OTLP to the same collector. Its inclusion in this trace is conditional
on verifying context propagation with the pinned SDK. OTLP export alone does not
prove correlation. If connected, it adds a fourth inference call without requiring
another model provider.

Trask shows two actual SQL queries:

1. A simple query using OTel GenAI conventions. It finds one model call; the
   application made four.
2. A query that works across the mixed trace, with the mappings and caveats
   needed to count calls, sum tokens, and attribute usage to the agent/tool.

Compare their results and highlight why the second query is more complicated:
different operation and token fields, ancestor relationships, and missing usage.

**Question:** What does "OpenTelemetry support" actually guarantee?

## 2. If I had a magic wand (4 min)

Liudmila describes the telemetry she wishes her team had. Trask connects each
wish to what the application would need. Present these as the desired experience,
not a claim that everything is supported today.

1. **One query across providers.** Consistent span naming, attributes, and
   operation names, regardless of who instrumented the library or how.
2. **Context flows through every layer.** LangChain picks up the HTTP server
   span's context and passes it through to native Azure SDK instrumentation.
3. **Configure OTLP once.** One export configuration for the application,
   rather than separate setup for LangSmith and the OTel SDK.
4. **One content policy.** Common configuration to enable content recording,
   sanitize it, and control its upload across instrumentations.
5. **Metrics and logs too.** Consistent support for metrics and logs alongside
   traces, so dashboards and investigations can use all three signals.

**Question:** How much of this can OpenTelemetry give us, and what work remains?

## 3. How we're addressing this in OpenTelemetry (8 min)

Switch from the application team's wish list to the work inside OTel. Liudmila
and Trask connect the pieces to the problems in the demo:

Start with what changed in 2026: OpenInference added opt-in OTel GenAI attributes,
OpenLLMetry migrated multiple instrumentations, and we started the first stabilization wave. Contrast
this progress with the early-2026 demo; identify the adoption scope and what is
being stabilized when preparing the slides.

Mention Arize's donation of OpenInference instrumentation code to OTel, expanding
SDK and framework coverage without starting from scratch. This is a code grant;
OpenInference remains a separate project.

1. **Semantic conventions define the schema.** Common operation and span names,
   attributes, and recording rules make telemetry comparable across providers.
   Show the scope: inference, tool execution, agents and workflows, embeddings,
   retrieval, and planning. Then connect it to what users measure: token usage,
   time to first chunk, duration, number of calls, errors, and error rates.
   Distinguish recorded signals from derived dashboard measures, and established
   coverage from conventions still being developed or stabilized.
2. **OTel instrumentations implement it.** Vendor-neutral instrumentation builds
   on OTel context propagation, configuration, and export, with traces, metrics,
   and logs. Distinguish what is available from what is still being built.
3. **Real frameworks challenge the design.** How do we support different SDKs
   and frameworks without flattening meaningful differences or inventing data
   instrumentation cannot capture?

Discuss native SDK instrumentation: authors know their libraries and can build
observability directly into them. It can also reflect SDK-specific choices;
maintainers may have limited OTel experience or time to track new OTel features.
Shared expectations and actionable feedback help native instrumentation evolve.

Use the dialogue to surface the pace and scope challenges:

- "By the time we agree, the framework has changed."
- "'Chat' is so 2023. What about agents, tools, and workflows?"
- "Is 'gen_ai' even what the cool kids call this anymore?"

**Trask:** "How do we keep up without making every reviewer an expert in every SDK?"

- **Give GenAI room to evolve.** GenAI conventions moved to a separate repo,
  with a somewhat different contributor community and greater reliance on
  AI-assisted workflows through `AGENTS.md`, instructions, and skills. Discuss
  independent versioning from core semconv as a way to match GenAI's pace.
  Reference scenarios ground proposals in actual library behavior.
- **Keep instrumentations thin.** The Python GenAI repo uses similar AI-assisted
  workflows. Each instrumentation adapts library-specific calls and results to
  the specialized `opentelemetry-util-genai` API. The utility owns common
  attribute mapping, span reporting, metrics, logs, configuration, and hooks.
  Show the small flow: library X → adapter → GenAI utility → OTel SDK.
- **Automate repeatable review checks.** Conformance tests check semconv
  compliance so reviewers can concentrate on capture correctness, library
  behavior, and edge cases. They reduce manual checking rather than replace
  review. Shared utility fixes benefit multiple instrumentations.

Progress as of November 1, 2026: four coordinated beta release rounds, plus
patch releases; 13 released instrumentation packages, up from five in the
first round. Refresh these numbers before the talk.

Community growth: 24 of 47 Python GenAI PR-author accounts made their first
merged PR in the OTel GitHub organization here. Since the repo's creation on
May 12, we merged 358 contributor-authored PRs, averaging about 15 per complete
week. Include the full weekly history in the research notes.

We're applying the Python approach in JavaScript too: migrating donated
OpenInference instrumentations into `opentelemetry-js-contrib`, with shared GenAI
utilities, conformance tests, and AI-assisted migration skills. This work is
in progress; JS stays in the existing contrib repo.

JS AI-related work brought in two additional first-time OTel merged-PR
contributors, bringing the combined newcomer count to 26. The research notes
list 15 merged JS AI-related PRs from eight authors in 2026.

Broaden the project timeline beyond Python/JS using the
[November 5 research expansion](kubecon-talk-research.md#2026-timeline-beyond-python-and-javascript).
Include Go's OpenAI/Anthropic compile-time instrumentation, Java's Spring AI
and MCP support, and OBI's model, tool, and retrieval coverage. Connect these
to the dedicated GenAI conventions repo, Collector normalization, conformance
tooling, and AAIF coordination. Distinguish merge dates, releases, and stability.
The research also verifies two newcomer examples in Go/OBI; it does not compute
an exhaustive cross-project contributor total.

**Question:** How do we know the instrumentations deliver what we agreed on?

## 4. How do we prove compatibility? (6 min)

Show conformance dashboards comparing instrumentations. One speaker explores
the results; the other explains how they are collected and what they mean.

- Compare emitted signals across instrumentations: spans, metrics, and logs.
- Drill into individual span types and their attributes to show coverage and
  conformance differences.
- Show how OTel Weaver Live Check validates emitted telemetry against formally
  defined conventions. The approach applies beyond GenAI to telemetry described
  in a supported semantic convention registry.
- Separate "was this signal emitted?" from "does the emitted signal conform?"
  Ground coverage expectations in the scenarios exercised.

Connect one dashboard finding to the application's query or interpretation.
Explain what the checks establish and what still needs behavioral validation.
Present conformance results as a feedback channel for instrumentation maintainers,
including native SDK authors: concrete gaps they can reproduce and address.

Return to the readiness report: validation now has visible, comparable evidence.

## 5. What's next? (3 min)

Return to the application's needs: "What would make the next dashboard easier?"
Discuss the direction of the work, without promising delivery dates:

- **Stability across signals.** Stabilize conventions for inference, agents,
  workflows, and tools across spans, metrics, and logs.
- **Stable instrumentations.** Move instrumentation packages toward stable releases.
- **Declarative configuration.** Improve support for configuring GenAI
  instrumentation through shared OTel declarative configuration.
- **More layers.** Represent arbitrary steps within agent and workflow execution.
- **More context on the data.** Carry conversation ID and the main agent's name
  onto relevant telemetry so users can query token usage per main agent without
  reconstructing the trace ancestry.
- **More use cases.** Cover hosted agents and harnesses, improve evaluation
  events, and describe guardrails.

## 6. A comparable experience with any instrumentation (2 min)

Return to the magic-wand wishes. Beyond the schema, highlight metrics and logs,
a content upload hook, and context propagation. Distinguish available features
from ongoing work and connect them to the application team's experience.

Celebrate the community making this possible: Arize donating instrumentation
code and adding OTel conventions to OpenInference, OpenLLMetry adopting OTel
conventions, Anthropic adding native SDK tracing with GenAI attributes, and
contributors working across project boundaries. Explain the user benefit:
fewer mappings, reusable dashboards, and less integration work. Verify the
specific adoption scope for the slides.

We see a need for OTel instrumentations today. The goal is a comparable user
experience with any instrumentation, whether maintained by OTel, a vendor, or
the SDK authors. The conventions, reference scenarios, and conformance tooling
exist to make that possible.

Close with appreciation for the community and an invitation to contribute real
scenarios, test instrumentations, and report gaps.

Evidence and adoption scope: [research notes](kubecon-talk-research.md).

## Questions (2 min)

## Demo preparation

Pin versions available by early 2026 and verify the mixed-schema trace. Prepare
initial and normalized query results, one conformance failure, and one real
AI-assisted development example. Exact packages and emitted fields remain to
be verified.

For LangSmith, verify exported attributes and cross-service parenting with the
pinned SDK. Its [OTel documentation](https://docs.langchain.com/langsmith/trace-with-opentelemetry#send-traces-to-an-alternate-provider)
supports alternate OTLP destinations from Python SDK 0.4.1. Inspect actual SDK
output; backend ingestion mappings do not establish what the exporter emits.
The [2025 context-propagation discussion](https://github.com/langchain-ai/langsmith-sdk/discussions/1851)
documents an initially export-only bridge, subsequent propagation work, and
remaining parenting reports. Verify both an OTel parent of a LangSmith run and
OTel children created inside that run before showing a connected trace.
