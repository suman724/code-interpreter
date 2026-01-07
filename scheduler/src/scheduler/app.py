from __future__ import annotations

from datetime import datetime
from typing import Dict

from fastapi import FastAPI, HTTPException

from .models import AllocateRequest, AllocateResponse, WorkerHeartbeat
from .store import WorkerStore

app = FastAPI(title="Scheduler")
store = WorkerStore()


@app.get("/v1/health")
def health() -> Dict[str, bool]:
    return {"ok": True}


@app.post("/v1/workers/heartbeat", response_model=WorkerHeartbeat)
def heartbeat(payload: WorkerHeartbeat) -> WorkerHeartbeat:
    payload.updated_at = datetime.utcnow()
    return store.record_heartbeat(payload)


@app.post("/v1/sessions/allocate", response_model=AllocateResponse)
def allocate(payload: AllocateRequest) -> AllocateResponse:
    allocation = store.allocate(payload)
    if not allocation:
        raise HTTPException(status_code=503, detail="No capacity available")
    return allocation
