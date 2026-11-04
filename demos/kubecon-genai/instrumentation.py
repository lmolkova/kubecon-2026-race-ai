"""Select the demo's instrumentation without changing application behavior."""

import os

MODE = os.getenv("DEMO_INSTRUMENTATION", "none")

if MODE == "otel":
    from opentelemetry.instrumentation.genai.langchain import LangChainInstrumentor
    from opentelemetry.instrumentation.genai.openai import OpenAIInstrumentor
elif MODE == "openinference":
    from openinference.instrumentation.langchain import LangChainInstrumentor
elif MODE == "langsmith":
    from langsmith.wrappers import wrap_openai
elif MODE != "none":
    raise ValueError(f"Unknown instrumentation: {MODE}")


def instrument(role):
    if role == "model-router":
        return
    if MODE in {"otel", "openinference"}:
        LangChainInstrumentor().instrument()
    if MODE == "otel" and role == "runbook":
        OpenAIInstrumentor().instrument()


def prepare_openai(client):
    return wrap_openai(client) if MODE == "langsmith" else client
