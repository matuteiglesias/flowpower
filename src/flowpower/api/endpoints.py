from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse
from flowpower.sdk.client import FlowpowerClient
from flowpower.engine.trace_utils import pretty_print_trace
from flowpower.api.chat_adapter import sse_adapter

router = APIRouter()
client = FlowpowerClient()

@router.post("/run")
def run_flow(flow_path: str = Form(...), data_path: str = Form(None)):
    run = client.run(flow=flow_path, data=data_path)
    return {"run_id": run.name, "status": run.status}

@router.get("/trace/{run_id}")
def get_trace(run_id: str):
    try:
        trace = client.trace(run_id)
        # You might replace this with a proper JSON schema
        return JSONResponse(content={
            "run_id": trace.name,
            "status": trace.status,
            "calls": len(getattr(trace, "api_calls", []))
        })
    except Exception as e:
        return JSONResponse(status_code=404, content={"error": str(e)})

@router.post("/chat")
def run_chat(flow_path: str = Form(...), user_input: str = Form(...)):
    generator = client.run(flow=flow_path, data={"question": user_input}, stream=True)
    return {"output": list(generator)}

@router.get("/stream")
def stream_chat(flow_path: str, user_input: str):
    generator = client.run(flow=flow_path, data={"question": user_input}, stream=True)
    return sse_adapter(generator)

@router.get("/describe")
def describe(flow_path: str):
    return client.describe(flow_path)
