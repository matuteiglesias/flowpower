# src/flowpower/api/server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from flowpower.sdk.client import FlowpowerClient
from flowpower.engine.trace_utils import pretty_print_trace

app = FastAPI()
client = FlowpowerClient()

# from fastapi import FastAPI
from flowpower.api.endpoints import router

# app = FastAPI()
app.include_router(router)


class RunRequest(BaseModel):
    flow_path: str
    data_path: Optional[str] = None
    column_mapping: Optional[dict] = None
    stream: Optional[bool] = False

class TraceRequest(BaseModel):
    run_id: str

@app.post("/run")
def run_flow(req: RunRequest):
    try:
        run = client.run(
            flow=req.flow_path,
            data=req.data_path,
            column_mapping=req.column_mapping,
            stream=req.stream,
        )
        return {"run_id": run.name, "status": run.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trace/{run_id}")
def trace_run(run_id: str):
    try:
        run = client.trace(run_id)
        # You can replace this with a structured return if needed
        return {
            "run_id": run.name,
            "status": run.status,
            "calls": getattr(run, "api_calls", [])
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Trace for run {run_id} not found: {e}")

@app.get("/health")
def health():
    return {"status": "ok"}
