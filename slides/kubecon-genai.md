<!-- layout: branded-cover -->

# The Race to Standardize AI Observability

Liudmila Molkova, Google · Trask Stalnaker, Microsoft

KubeCon + CloudNativeCon North America 2026

---

# “Trask, can you help with the dashboard?”

- [x] Instrumentation installed
- [x] OTLP export configured
- [x] Traces arriving
- [ ] Dashboard
- [ ] Validation

---

# Our expectations

![Expected waterfall with capture-aligned timing: workflow, diagnostic agent, and HTTP client/server spans connecting the runbook service](assets/expected-waterfall.svg)

---

# The reality

![All 22 spans from the saved Aspire trace, redrawn as a waterfall with captured nesting, services, and timing](assets/aspire-waterfall.svg)

---

# Querying token usage

```sql
SELECT COUNT(*) AS calls,
  SUM("gen_ai.usage.input_tokens") AS input_tokens
FROM span_data
WHERE trace_id = :trace_id
  AND "gen_ai.operation.name" = 'chat';
```

**2 calls · 280 input tokens**

---

# Dashboard usage vs. reality

![Live query estimate versus delayed provider billing](assets/usage-vs-bill.svg)

---

# How did we instrument the application?

![Workflow, diagnostic agent, and runbook service with OpenInference, native OTel, and LangSmith OTLP instrumentation](assets/instrumentation-architecture.svg)

---

# Accounting for different schemas

```sql
WITH calls AS (
  SELECT COALESCE(
    "gen_ai.usage.input_tokens",
    "llm.token_count.prompt"
  ) AS input_tokens
  FROM span_data WHERE trace_id = :trace_id AND (
    "gen_ai.operation.name" = 'chat'
    OR lower("openinference.span.kind") = 'llm'
    OR lower("langsmith.span.kind") = 'llm'
  )
)
SELECT COUNT(*) AS calls, SUM(input_tokens) AS input_tokens,
       SUM(input_tokens IS NULL) AS missing_usage FROM calls;
```

**5 inference spans · 900 input tokens · 0 missing usage values**

---

# Where context gets lost

![Full trace with the runbook subtree boxed and an arrow to consult_runbook; separate orphan HTTP trace with an arrow to the runbook ChatOpenAI span](assets/aspire-parent-gap.svg)

---

# If I had a magic wand

- One schema across all instrumentations
- Proper correlation between them
- Traces, metrics, and logs
- One config for content capture
- Large content separate from telemetry, but reacheable

---

# What did we do in OTel

<table>
<thead><tr><th>Wish</th><th class="fragment" data-fragment="otel">OpenTelemetry</th></tr></thead>
<tbody>
<tr><td>One schema across all<br>instrumentations</td><td class="fragment" data-fragment="otel">GenAI semantic conventions, checked by conformance tests</td></tr>
<tr><td>Proper correlation between them</td><td class="fragment" data-fragment="otel">Context propagation</td></tr>
<tr><td>Traces, metrics, and logs</td><td class="fragment" data-fragment="otel">One SDK and OTLP for all three signals</td></tr>
<tr><td>One config for content capture</td><td class="fragment" data-fragment="otel">A shared content-capture setting</td></tr>
<tr><td>Large content separate from telemetry,<br>while still reachable</td><td class="fragment" data-fragment="otel">An upload hook that stores content and links to it</td></tr>
</tbody>
</table>

---

# GenAI semantic conventions

New home: [semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai)

![GenAI trace waterfall; bold operations target stability, HTTP and DB use core conventions](assets/semconv-waterfall.svg)

<p style="margin: -20px 0 0 28px; font-size: 22px; color: var(--cp-text-muted);"><strong>Bold</strong>: stability targets</p>

---

# GenAI attributes

<div style="display: flex; align-items: center; gap: 24px;">
<div style="flex: 0 0 26%;">
<ul class="attr-key">
<li style="--c: #d64545;">Agent / workflow identity</li>
<li style="--c: #425cc7;">Model details and request parameters</li>
<li style="--c: #f5a800;">Token usage</li>
<li style="--c: #0f8188;">Inputs, outputs, and instructions</li>
<li style="--c: #a3367a;">Tool definitions, calls, and results</li>
</ul>
</div>
<div style="flex: 1; min-width: 0;">
<table class="attr-table" aria-label="GenAI attributes from the demo trace">
<tr style="--c: #d64545;"><th scope="row">gen_ai.agent.name</th><td>diagnostic</td></tr>
<tr style="--c: #425cc7;"><th scope="row">gen_ai.operation.name</th><td>chat</td></tr>
<tr style="--c: #425cc7;"><th scope="row">gen_ai.provider.name</th><td>openai</td></tr>
<tr style="--c: #425cc7;"><th scope="row">gen_ai.request.model</th><td>gpt-4.1</td></tr>
<tr style="--c: #425cc7;"><th scope="row">gen_ai.response.model</th><td>gpt-4.1</td></tr>
<tr style="--c: #425cc7;"><th scope="row">gen_ai.response.id</th><td>chatcmpl-4021efaa4f924ee6a425ecde938da86d</td></tr>
<tr style="--c: #425cc7;"><th scope="row">gen_ai.response.finish_reasons</th><td>["tool_calls"]</td></tr>
<tr style="--c: #f5a800;"><th scope="row">gen_ai.usage.input_tokens</th><td>120</td></tr>
<tr style="--c: #f5a800;"><th scope="row">gen_ai.usage.output_tokens</th><td>30</td></tr>
<tr style="--c: #0f8188;"><th scope="row">gen_ai.input.messages</th><td class="wrap">[{"role":"user","parts":[{"content":"Why is checkout restarting, and what should I do?","type":"text"}]}]</td></tr>
<tr style="--c: #0f8188;"><th scope="row">gen_ai.output.messages</th><td class="wrap">[{"role":"assistant","parts":[{"arguments":{"workload":"checkout"},"name":"inspect_workload","type":"tool_call"}]}]</td></tr>
<tr style="--c: #a3367a;"><th scope="row">gen_ai.tool.definitions</th><td class="wrap">[{"name":"inspect_workload","description":"Inspect Kubernetes evidence for a workload."}]</td></tr>
</table>
</div>
</div>

---

# Structured inputs and outputs

`gen_ai.input.messages`

```json
[{"role": "user", "parts": [{
  "type": "text",
  "content": "Why is checkout restarting, and what should I do?"
}]}]
```

`gen_ai.output.messages`

```json
[{"role": "assistant", "finish_reason": "tool_calls", "parts": [
  {"type": "tool_call", "id": "call_diagnose",
   "name": "inspect_workload", "arguments": {"workload": "checkout"}},
  {"type": "tool_call", "id": "call_runbook",
   "name": "consult_runbook", "arguments": {"topic": "OOMKilled"}}
]}]
```

---

# Conversation and tool results

<div class="aspire" role="group" aria-label="Aspire-style view of the final inference span">
<div class="aspire-header"><span class="aspire-title">diagnostic-agent: chat gpt-4.1</span><span class="aspire-span-id">6483b37</span><span class="aspire-llm">LLM</span><span class="aspire-tabs"><span class="active">Input &amp; output</span><span>Tools 2</span><span>Details</span></span><span class="aspire-stats">Duration <b>1.88ms</b> · Tokens <b>360</b></span></div>
<div class="aspire-body">
<p class="aspire-section">Input</p>
<div class="aspire-grid">
<div class="aspire-col-left">
<div class="aspire-card"><span class="aspire-role aspire-user">User</span><span class="aspire-badge message">&#9993; Message</span><div class="aspire-content">Why is checkout restarting, and what should I do?</div></div>
<div class="aspire-card"><span class="aspire-role aspire-assistant">Assistant</span><span class="aspire-badge tool-calls">&lt;/&gt; Tool calls</span><div class="aspire-content"><span class="fn">inspect_workload</span>({"workload": <span class="str">"checkout"</span>})
<span class="fn">consult_runbook</span>({"topic": <span class="str">"OOMKilled"</span>})</div></div>
<p class="aspire-section aspire-output-heading">Output</p>
</div>
<div>
<div class="aspire-card"><span class="aspire-role aspire-user">User</span><span class="aspire-badge tool-response">&#9993; Tool response</span><div class="aspire-content">{"evidence": <span class="str">"checkout was OOMKilled; memory limit is 128Mi and peak usage is 192Mi."</span>}</div></div>
<div class="aspire-card"><span class="aspire-role aspire-user">User</span><span class="aspire-badge tool-response">&#9993; Tool response</span><div class="aspire-content">{"recommendation": <span class="str">"Inspect the memory regression; raise the limit only after checking cluster capacity."</span>}</div></div>
</div>
</div>
<div class="aspire-card" style="margin-bottom: 0;"><span class="aspire-role aspire-assistant">Assistant</span><span class="aspire-badge output">&#9993; Output</span><div class="aspire-content">Checkout exceeded its 128Mi memory limit. Investigate the regression and review capacity before changing limits.</div></div>
</div>
</div>

---

# Usage, latency, and errors

<table>
<thead><tr><th>Dashboard question</th><th class="fragment" data-fragment="data">Recorded data</th></tr></thead>
<tbody>
<tr><td>Where did the tokens go?</td><td class="fragment" data-fragment="data">Input + output tokens</td></tr>
<tr><td>How much usage involved caching?</td><td class="fragment" data-fragment="data">Cache read + cache creation tokens</td></tr>
<tr><td>How much was text, image, or audio?</td><td class="fragment" data-fragment="data">Tokens by modality</td></tr>
<tr><td>How quickly did streaming begin?</td><td class="fragment" data-fragment="data">Time to first chunk</td></tr>
<tr><td>Which operation was slow?</td><td class="fragment" data-fragment="data">Duration</td></tr>
<tr><td>How often does this fail?</td><td class="fragment" data-fragment="data">Calls + errors</td></tr>
</tbody>
</table>

---

<!-- layout: branded-transition -->

# From conventions to instrumentation

---

# OpenInference instrumentation donation

**June 16, 2026 · Arize's code donation merged into OTel**

- The community is adopting and adapting the donated instrumentations
- Making them fully vendor-neutral with OTel conventions, configuration, and APIs

---

# How we build instrumentations

New repo: [opentelemetry-python-genai](https://github.com/open-telemetry/opentelemetry-python-genai)

- Shared GenAI Util: spans, metrics, content, context
- Thin adapters: provider data → GenAI Util
- Conformance checks + unit tests
- AI-assisted development and review

```python
with handler.inference("openai", request_model=kwargs["model"]) as operation:
    response = wrapped(*args, **kwargs)
    operation.response_model_name = response.model
    set_usage(operation, response.usage)
    if handler.should_capture_content():
        operation.output_messages = _prepare_output_messages(response.choices)
    return response
```

---

# More contributors, faster delivery

- **26 newcomers to OTel** across Python GenAI + JS AI work
- **13 Python instrumentation packages · 4 beta release rounds**
- JS is adopting the shared-utility and conformance approach

<img src="assets/python-genai-contributions-monthly.svg" alt="Python GenAI instrumentation PRs merged per month: 0 to 19 a month in python-contrib from November 2024, rising to 116 in September 2026 after the python-genai repository launched in May 2026" style="display: block; width: 100%; object-fit: contain; margin: 12px auto 0;" />

---

# Native SDK instrumentation

- Anthropic tracing, ADK, Azure AI libraries
- MCP Python and .NET, Mistral, LangChain, and many others
- Native instrumentation is good for users and the ecosystem
- Need a way to lib developers to validate conformance

---

<!-- layout: branded-transition -->

# Every instrumentation needs conformance tests

---

# Conformance testing with Weaver

[open-telemetry/semantic-conventions-conformance](https://github.com/open-telemetry/semantic-conventions-conformance)

<div class="code-grid" style="display: grid; grid-template-columns: auto auto auto; gap: 24px; align-items: start;">
<div>

**1. Run a library scenario**

```python
from openai import OpenAI

OpenAI().chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": "Say hello",
    }],
)
```

</div>
<div>

**2. Check emitted telemetry**

```sh
weaver registry live-check \
  --registry ./registry \
  --input-source otlp \
  --format json \
  --no-stream \
  --output ./report
```

</div>
<div>

**3. Compare `data.json`**

```json
{
  "spans": {
    "gen_ai.inference.client": [
      "gen_ai.operation.name",
      "gen_ai.request.model",
      "gen_ai.usage.input_tokens",
      "gen_ai.usage.output_tokens"
    ]
  },
  "findings": []
}
```

</div>
</div>

---

# Comparing instrumentation output

TODO: Find a better screenshot.

![Inference attribute comparison across Anthropic instrumentations](assets/conformance-inference.png)

---

# Adoption across the community

| Project | Progress in 2026 |
| --- | --- |
| Arize / OpenInference | OTel GenAI opt-in flag |
| Anthropic | Native SDK tracing with GenAI attributes |
| OpenLLMetry | GenAI convention adoption |
| OpenTelemetry | Instrumentations, shared utilities, conformance |

---

# Next: stability and adoption

- Initial wave: inference, agents/workflows, and tools across signals
- After: stabilize incrementally, feature by feature
- Improve instrumentation coverage and ergonomics

---

# Next: richer agent telemetry

- Trace steps, skills, and realtime interactions
- Propagate conversation IDs and agent details in context - enable better cost / usage analysis on operation level
- Capture evaluations and guardrail outcomes
- Cover hosted agents and harnesses
- 

---

# How to contribute

TODO

# Thank you!

<div style="display: flex; align-items: center; gap: 56px;">
<img src="assets/the-race-to-standardize-ai-observability_molkova-stalnaker_1246166_feedback-code.png" alt="Scan to leave feedback on The Race to Standardize AI Observability" style="width: 340px; height: 340px; margin: 0; flex-shrink: 0;" />
<div>
<p><a href="https://github.com/open-telemetry/semantic-conventions-genai">GenAI conventions</a></p>
<p><a href="https://github.com/open-telemetry/semantic-conventions-conformance">Conformance repository</a></p>
<p><a href="https://open-telemetry.github.io/semantic-conventions-conformance/">Conformance reports</a></p>
</div>
</div>
