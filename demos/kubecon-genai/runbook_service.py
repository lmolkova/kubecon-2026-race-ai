"""Runbook service shared by both instrumentation setups."""

import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from langgraph.graph import END, START, StateGraph
from openai import OpenAI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from instrumentation import instrument, prepare_openai
from telemetry import configure

MODEL_ROUTER = os.getenv("MODEL_URL", "http://localhost:8001")
logger = logging.getLogger("demo")


def create_app():
    providers = configure()
    instrument("runbook")
    HTTPXClientInstrumentor().instrument()

    @asynccontextmanager
    async def lifespan(app):
        yield
        for provider in providers:
            provider.force_flush()
            provider.shutdown()

    app = FastAPI(title="Runbook", lifespan=lifespan,
                  telemetry={"tracing": False, "metrics": False, "logs": False})
    FastAPIInstrumentor.instrument_app(
        app, excluded_urls="/health", exclude_spans=["receive", "send"]
    )

    @app.get("/health")
    def health():
        return {"status": "ok"}

    def call_model(payload: dict):
        with OpenAI(base_url=MODEL_ROUTER + "/v1", api_key="local-only", max_retries=0,
                    default_headers={"x-demo-run-id": payload["run_id"]}) as raw:
            client = prepare_openai(raw)
            result = client.chat.completions.create(model="gpt-6-luna", messages=[
                {"role": "user", "content": f"Recommend remediation for {payload['topic']}."}])
        logger.info("Runbook recommendation returned")
        return {"recommendation": result.choices[0].message.content}

    builder = StateGraph(dict)
    builder.add_node("model", call_model)
    builder.add_edge(START, "model")
    builder.add_edge("model", END)
    graph = builder.compile(name="runbook")

    @app.post("/runbook")
    def runbook(payload: dict):
        return graph.invoke(payload)

    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
