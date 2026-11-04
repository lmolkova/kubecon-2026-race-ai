CREATE TABLE IF NOT EXISTS spans (
    trace_id TEXT, span_id TEXT PRIMARY KEY, parent_id TEXT,
    service TEXT, scope TEXT, name TEXT, kind TEXT, status TEXT,
    start_ns INTEGER, end_ns INTEGER, attrs TEXT, events TEXT
);
CREATE VIEW IF NOT EXISTS span_data AS
SELECT *,
    json_extract(attrs, '$."gen_ai.operation.name"') AS "gen_ai.operation.name",
    json_extract(attrs, '$."gen_ai.request.model"') AS "gen_ai.request.model",
    json_extract(attrs, '$."gen_ai.usage.input_tokens"') AS "gen_ai.usage.input_tokens",
    json_extract(attrs, '$."gen_ai.usage.output_tokens"') AS "gen_ai.usage.output_tokens",
    json_extract(attrs, '$."gen_ai.usage.prompt_tokens"') AS "gen_ai.usage.prompt_tokens",
    json_extract(attrs, '$."gen_ai.usage.completion_tokens"') AS "gen_ai.usage.completion_tokens",
    json_extract(attrs, '$."gen_ai.agent.name"') AS "gen_ai.agent.name",
    json_extract(attrs, '$."gen_ai.tool.name"') AS "gen_ai.tool.name",
    json_extract(attrs, '$."openinference.span.kind"') AS "openinference.span.kind",
    json_extract(attrs, '$."langsmith.span.kind"') AS "langsmith.span.kind",
    json_extract(attrs, '$."llm.model_name"') AS "llm.model_name",
    json_extract(attrs, '$."llm.token_count.prompt"') AS "llm.token_count.prompt",
    json_extract(attrs, '$."llm.token_count.completion"') AS "llm.token_count.completion",
    json_extract(attrs, '$."tool.name"') AS "tool.name",
    json_extract(attrs, '$."langfuse.observation.type"') AS "langfuse.observation.type",
    json_extract(attrs, '$."langfuse.observation.model.name"') AS "langfuse.observation.model.name",
    json_extract(attrs, '$."langfuse.observation.usage_details"."input"') AS "langfuse.observation.usage_details.input",
    json_extract(attrs, '$."langfuse.observation.usage_details"."output"') AS "langfuse.observation.usage_details.output",
    json_extract(json_extract(attrs, '$."http.response.header.x_demo_run_id"'), '$[0]') AS demo_run_id
FROM spans;
