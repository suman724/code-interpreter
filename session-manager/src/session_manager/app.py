from __future__ import annotations

from datetime import datetime
from typing import Dict

from fastapi import FastAPI, HTTPException

from .models import IdempotencyRecord, SessionRecord
from .storage import InMemorySessionStore

app = FastAPI(title="Session Manager")
store = InMemorySessionStore()


@app.get("/v1/health")
def health() -> Dict[str, bool]:
    return {"ok": True}


@app.post("/v1/sessions", response_model=SessionRecord, status_code=201)
def create_session(record: SessionRecord) -> SessionRecord:
    return store.create_session(record)


@app.get("/v1/sessions/{session_id}", response_model=SessionRecord)
def get_session(session_id: str) -> SessionRecord:
    try:
        return store.get_session(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Session not found") from exc


@app.patch("/v1/sessions/{session_id}/routing", response_model=SessionRecord)
def update_routing(session_id: str, worker_endpoint: str, sandbox_id: str | None = None) -> SessionRecord:
    try:
        return store.update_routing(session_id, worker_endpoint, sandbox_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Session not found") from exc


@app.delete("/v1/sessions/{session_id}", status_code=204)
def delete_session(session_id: str) -> None:
    if session_id not in store.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    store.mark_stopped(session_id)


@app.post("/v1/idempotency")
def put_idempotency(record: IdempotencyRecord) -> Dict[str, str]:
    store.save_idempotency(record)
    return {"status": "saved", "idempotency_key": record.idempotency_key}


@app.get("/v1/idempotency/{idempotency_key}")
def get_idempotency(idempotency_key: str) -> Dict[str, object]:
    record = store.get_idempotency(idempotency_key)
    if not record:
        raise HTTPException(status_code=404, detail="Idempotency key not found")
    return record.dict()


@app.post("/v1/reaper")
def reap_sessions() -> Dict[str, int]:
    count = store.reap_expired()
    return {"reaped": count, "timestamp": datetime.utcnow().isoformat()}
