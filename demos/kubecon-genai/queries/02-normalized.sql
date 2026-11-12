WITH RECURSIVE
classified AS (
    SELECT *,
        CASE
            WHEN "gen_ai.operation.name" IN
                 ('chat', 'generate_content', 'text_completion') THEN 'inference'
            WHEN lower("openinference.span.kind") = 'llm'
                 OR lower("langsmith.span.kind") = 'llm'
                 OR "langfuse.observation.type" = 'generation'
                 THEN 'inference'
            WHEN "gen_ai.operation.name" = 'invoke_agent'
                 OR "langfuse.observation.type" = 'agent'
                 OR lower("openinference.span.kind") = 'agent'
                 THEN 'agent'
            WHEN "gen_ai.operation.name" = 'execute_tool'
                 OR "langfuse.observation.type" = 'tool'
                 OR lower("openinference.span.kind") = 'tool'
                 OR lower("langsmith.span.kind") = 'tool'
                 THEN 'tool'
        END AS operation,
        COALESCE(
            "gen_ai.request.model",
            "llm.model_name",
            "langfuse.observation.model.name"
        ) AS model,
        COALESCE(
            "gen_ai.usage.input_tokens",
            "llm.token_count.prompt",
            "gen_ai.usage.prompt_tokens",
            "langfuse.observation.usage_details.input"
        ) AS input_tokens,
        COALESCE(
            "gen_ai.usage.output_tokens",
            "llm.token_count.completion",
            "gen_ai.usage.completion_tokens",
            "langfuse.observation.usage_details.output"
        ) AS output_tokens
    FROM span_data
    WHERE trace_id = :trace_id
),
ancestry AS (
    SELECT span_id AS inference_id, parent_id AS ancestor_id, 1 AS depth
    FROM classified WHERE operation = 'inference'
    UNION ALL
    SELECT a.inference_id, p.parent_id, a.depth + 1
    FROM ancestry a JOIN classified p ON p.span_id = a.ancestor_id
    WHERE p.parent_id IS NOT NULL AND a.depth < 64
),
attributed AS (
    SELECT s.*,
        (SELECT COALESCE(p."gen_ai.agent.name", p.name)
         FROM ancestry a JOIN classified p ON p.span_id = a.ancestor_id
         WHERE a.inference_id = s.span_id AND p.operation = 'agent'
         ORDER BY a.depth DESC LIMIT 1) AS main_agent,
        (SELECT COALESCE(p."gen_ai.tool.name",
                         p."tool.name", p.name)
         FROM ancestry a JOIN classified p ON p.span_id = a.ancestor_id
         WHERE a.inference_id = s.span_id AND p.operation = 'tool'
         ORDER BY a.depth LIMIT 1) AS tool
    FROM classified s WHERE operation = 'inference'
)
SELECT main_agent, tool, model, COUNT(*) AS model_calls,
       SUM(input_tokens) AS input_tokens, SUM(output_tokens) AS output_tokens,
       SUM(input_tokens IS NULL) AS calls_missing_input_usage,
       SUM(output_tokens IS NULL) AS calls_missing_output_usage
FROM attributed
GROUP BY main_agent, tool, model
ORDER BY main_agent, tool, model;
