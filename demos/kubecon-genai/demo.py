"""A real SDK integration demo with deterministic, local model APIs."""

import argparse
import logging
import os
import uuid
from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from instrumentation import instrument
from telemetry import configure

MODEL_ROUTER = os.getenv("MODEL_URL", "http://localhost:8001")
RUNBOOK = os.getenv("RUNBOOK_URL", "http://localhost:8002")
logger = logging.getLogger("demo")


def create_app(role):
    providers = configure() if role != "model-router" else ()
    instrument(role)

    @asynccontextmanager
    async def lifespan(app):
        yield
        for provider in providers:
            provider.force_flush()
            provider.shutdown()

    app = FastAPI(title="KubeCon telemetry demo: " + role, lifespan=lifespan,
                  telemetry={"tracing": False, "metrics": False, "logs": False})
    if role != "model-router":
        FastAPIInstrumentor.instrument_app(
            app, excluded_urls="/health", exclude_spans=["receive", "send"]
        )
        HTTPXClientInstrumentor().instrument()

    @app.get("/health")
    def health():
        return {"status": "ok", "role": role}

    if role == "model-router":
        requests = {}

        @app.get("/requests/{run_id}")
        def request_records(run_id: str):
            return requests.get(run_id, [])

        @app.post("/v1/chat/completions")
        @app.post("/v1/messages")
        async def completion(request: Request):
            body = await request.json()
            model = body["model"]
            run_id = request.headers.get("x-demo-run-id", "unknown")
            response_id = "chatcmpl-" + uuid.uuid4().hex
            if request.headers.get("x-demo-fail") == "true":
                requests.setdefault(run_id, []).append({
                    "model": model, "status": 503, "input_tokens": None, "output_tokens": None})
                return JSONResponse({"type": "error", "error": {"message": "Injected local model outage", "type": "api_error"}}, status_code=503)
            if model == "claude-sonnet-4-6":
                tokens, text = (200, 50), "checkout was OOMKilled; memory limit is 128Mi and peak usage is 192Mi."
            elif model == "gpt-4.1-mini":
                tokens, text = (80, 20), "Inspect the memory regression; raise the limit only after checking cluster capacity."
            elif any(m.get("role") == "tool" for m in body["messages"]):
                tokens, text = (300, 60), "Checkout exceeded its 128Mi memory limit. Investigate the regression and review capacity before changing limits."
            else:
                tokens, text = (120, 30), None
            message = {"role": "assistant", "content": text}
            if text is None:
                message["tool_calls"] = [
                    {"id": "call_diagnose", "type": "function", "function": {
                        "name": "inspect_workload", "arguments": '{"workload":"checkout"}'}},
                    {"id": "call_runbook", "type": "function", "function": {
                        "name": "consult_runbook", "arguments": '{"topic":"OOMKilled"}'}},
                ]
            if text is None and request.headers.get("x-demo-fail-tool") == "true":
                message["tool_calls"] = message["tool_calls"][:1]
            requests.setdefault(run_id, []).append({
                "model": model, "status": 200, "input_tokens": tokens[0], "output_tokens": tokens[1]})
            if request.url.path == "/v1/messages":
                return {"id": response_id, "type": "message", "role": "assistant",
                        "model": model, "content": [{"type": "text", "text": text}],
                        "stop_reason": "end_turn", "stop_sequence": None,
                        "usage": {"input_tokens": tokens[0], "output_tokens": tokens[1]}}
            return {"id": response_id, "object": "chat.completion", "created": 1700000000,
                    "model": model, "choices": [{"index": 0, "message": message,
                    "finish_reason": "tool_calls" if text is None else "stop"}],
                    "usage": {"prompt_tokens": tokens[0], "completion_tokens": tokens[1],
                              "total_tokens": sum(tokens)}}

    if role == "agent":
        @app.post("/run")
        def run(payload: dict):
            scenario = payload.get("scenario", "mixed")
            if scenario not in {"mixed", "tool-error"}:
                return JSONResponse({"error": "Use mixed or tool-error"}, status_code=400)
            run_id = uuid.uuid4().hex
            messages = [{"role": "user", "content": "Why is checkout restarting, and what should I do?"}]
            result = {"run_id": run_id, "scenario": scenario}
            try:
                logger.info("Starting diagnosis", extra={"demo.run_id": run_id, "demo.scenario": scenario})
                @tool
                def inspect_workload(workload: str) -> dict:
                    """Inspect Kubernetes evidence for a workload."""
                    logger.info("Inspecting checkout: OOMKilled, limit 128Mi, peak 192Mi")
                    model = ChatAnthropic(
                        model="claude-sonnet-4-6", base_url=MODEL_ROUTER,
                        api_key="local-only", max_retries=0, max_tokens=256,
                        default_headers={"x-demo-run-id": run_id,
                                         "x-demo-fail": str(scenario == "tool-error").lower()},
                    )
                    diagnostic = create_agent(
                        model=model, name="diagnostic",
                        system_prompt="Summarize Kubernetes evidence.",
                    )
                    state = diagnostic.invoke({"messages": [{
                        "role": "user", "content":
                        f"{workload}: OOMKilled; memory limit 128Mi; peak 192Mi.",
                    }]})
                    return {"evidence": state["messages"][-1].content}

                @tool
                def consult_runbook(topic: str) -> dict:
                    """Consult the runbook for a Kubernetes failure."""
                    with httpx.Client() as client:
                        response = client.post(RUNBOOK + "/runbook", json={
                            "run_id": run_id, "topic": topic})
                        response.raise_for_status()
                        return response.json()

                with httpx.Client() as model_http:
                    model = ChatOpenAI(
                        model="gpt-4.1", base_url=MODEL_ROUTER + "/v1",
                        api_key="local-only", max_retries=0,
                        use_responses_api=False, http_client=model_http,
                        default_headers={"x-demo-run-id": run_id,
                            "x-demo-fail-tool": str(scenario == "tool-error").lower()},
                    )
                    tools = [inspect_workload, consult_runbook]
                    model_with_tools = model.bind_tools(tools)

                    def call_model(state: MessagesState):
                        return {"messages": [model_with_tools.invoke(state["messages"])]}

                    builder = StateGraph(MessagesState)
                    builder.add_node("model", call_model)
                    builder.add_node("tools", ToolNode(tools, handle_tool_errors=False))
                    builder.add_edge(START, "model")
                    builder.add_conditional_edges("model", tools_condition)
                    builder.add_edge("tools", "model")
                    workflow = builder.compile(name="diagnose_workload")
                    state = workflow.invoke({"messages": messages})
                    result["answer"] = state["messages"][-1].content
            except Exception as exc:
                logger.exception("Diagnosis failed", extra={"demo.run_id": run_id})
                result["error"] = str(exc)
            return JSONResponse(result, status_code=502 if "error" in result else 200,
                                headers={"x-demo-run-id": run_id})

    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["serve"])
    parser.add_argument("role", choices=["model-router", "agent"])
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(create_app(args.role), host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
