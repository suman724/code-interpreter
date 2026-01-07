from __future__ import annotations

from datetime import datetime
from typing import Dict

from fastapi import FastAPI, HTTPException, Request, Response

from .models import (
    CommandRequest,
    Execution,
    ExecutionCreateRequest,
    FileCommitRequest,
    FileDownloadUrlRequest,
    FileDownloadUrlResponse,
    FileUploadUrlRequest,
    FileUploadUrlResponse,
    MetricsResponse,
    Session,
    SessionCreateRequest,
)
from .storage import InMemoryStore

app = FastAPI(title="Code Interpreter Control Plane")
store = InMemoryStore()


@app.get("/v1/health")
def health() -> Dict[str, bool]:
    return {"ok": True}


@app.post("/v1/sessions", status_code=201, response_model=Session)
def create_session(payload: SessionCreateRequest) -> Session:
    return store.create_session(payload)


@app.get("/v1/sessions/{session_id}", response_model=Session)
def get_session(session_id: str) -> Session:
    try:
        return store.get_session(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Session not found") from exc


@app.delete("/v1/sessions/{session_id}", status_code=204)
def delete_session(session_id: str) -> Response:
    if session_id not in store.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    store.delete_session(session_id)
    return Response(status_code=204)


@app.post("/v1/sessions/{session_id}/executions", response_model=Execution)
def execute_code(session_id: str, payload: ExecutionCreateRequest) -> Execution:
    if session_id not in store.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return store.execute_code(session_id, payload)


@app.post("/v1/sessions/{session_id}/commands", response_model=Execution)
def run_command(session_id: str, payload: CommandRequest) -> Execution:
    if session_id not in store.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return store.run_command(session_id, payload)


@app.get("/v1/executions/{execution_id}", response_model=Execution)
def get_execution(execution_id: str) -> Execution:
    try:
        return store.get_execution(execution_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Execution not found") from exc


@app.get("/v1/executions/{execution_id}/events")
def execution_events(execution_id: str) -> Dict[str, str]:
    if execution_id not in store.executions:
        raise HTTPException(status_code=404, detail="Execution not found")
    return {"message": "streaming not implemented"}


@app.post("/v1/sessions/{session_id}/files:upload-url", response_model=FileUploadUrlResponse)
def upload_url(session_id: str, payload: FileUploadUrlRequest) -> FileUploadUrlResponse:
    if session_id not in store.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return FileUploadUrlResponse(
        upload_url="https://example.com/upload",
        object_key=f"{session_id}{payload.path}",
        headers={"Content-Type": payload.content_type},
    )


@app.post("/v1/sessions/{session_id}/files:commit")
def commit_upload(session_id: str, payload: FileCommitRequest) -> Dict[str, bool]:
    if session_id not in store.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"ok": True}


@app.post("/v1/sessions/{session_id}/files:download-url", response_model=FileDownloadUrlResponse)
def download_url(session_id: str, payload: FileDownloadUrlRequest) -> FileDownloadUrlResponse:
    if session_id not in store.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return FileDownloadUrlResponse(download_url="https://example.com/download")


@app.put("/v1/sessions/{session_id}/files/{path:path}")
async def put_file(session_id: str, path: str, request: Request) -> Dict[str, object]:
    if session_id not in store.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        data = await request.body()
        bytes_written = store.put_file(session_id, f"/{path.lstrip('/')}", data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "bytes_written": bytes_written}


@app.get("/v1/sessions/{session_id}/files/{path:path}")
def get_file(session_id: str, path: str) -> Response:
    if session_id not in store.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        data = store.get_file(session_id, f"/{path.lstrip('/')}")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return Response(content=data, media_type="application/octet-stream")


@app.get("/v1/sessions/{session_id}/metrics", response_model=MetricsResponse)
def session_metrics(session_id: str) -> MetricsResponse:
    if session_id not in store.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return MetricsResponse(
        cpu_usage_percent=0.0,
        memory_usage_mib=0.0,
        disk_usage_bytes=0,
        running=True,
    )


@app.get("/")
def root() -> Dict[str, str]:
    return {"service": "control-plane-api", "timestamp": datetime.utcnow().isoformat()}
