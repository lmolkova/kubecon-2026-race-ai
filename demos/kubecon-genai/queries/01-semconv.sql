SELECT
    COUNT(*) AS model_calls,
    SUM("gen_ai.usage.input_tokens") AS input_tokens,
    SUM("gen_ai.usage.output_tokens") AS output_tokens
FROM span_data
WHERE trace_id = :trace_id
  AND "gen_ai.operation.name" = 'chat';
