from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict
from uuid import uuid4

from .models import (
    CommandRequest,
    Execution,
    ExecutionCreateRequest,
    ExecutionStatus,
    Session,
    SessionCreateRequest,
    SessionState,
)


@dataclass
class InMemoryStore:
    sessions: Dict[str, Session] = field(default_factory=dict)
    executions: Dict[str, Execution] = field(default_factory=dict)
    files: Dict[str, Dict[str, bytes]] = field(default_factory=dict)

    def create_session(self, request: SessionCreateRequest) -> Session:
        session_id = f"sess_{uuid4().hex[:8]}"
        now = datetime.utcnow()
        session = Session(
            session_id=session_id,
            state=SessionState.READY,
            created_at=now,
            expires_at=now + timedelta(seconds=request.ttl_seconds),
            idle_expires_at=now + timedelta(seconds=request.idle_timeout_seconds),
            runtime=request.runtime,
            resources=request.resources,
            egress_policy=request.egress_policy,
        )
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Session:
        return self.sessions[session_id]

    def delete_session(self, session_id: str) -> None:
        session = self.sessions.get(session_id)
        if session:
            session.state = SessionState.STOPPED
            self.sessions[session_id] = session
            self.files.pop(session_id, None)

    def _create_execution(self, session_id: str) -> Execution:
        execution_id = f"exec_{uuid4().hex[:8]}"
        execution = Execution(
            execution_id=execution_id,
            session_id=session_id,
            status=ExecutionStatus.COMPLETED,
            created_at=datetime.utcnow(),
            started_at=datetime.utcnow(),
            finished_at=datetime.utcnow(),
            stdout="",
            stderr="",
            has_error=False,
            exit_code=0,
        )
        self.executions[execution_id] = execution
        return execution

    def execute_code(self, session_id: str, request: ExecutionCreateRequest) -> Execution:
        return self._create_execution(session_id)

    def run_command(self, session_id: str, request: CommandRequest) -> Execution:
        return self._create_execution(session_id)

    def get_execution(self, execution_id: str) -> Execution:
        return self.executions[execution_id]

    @staticmethod
    def validate_workspace_path(path: str) -> str:
        if "\x00" in path:
            raise ValueError("Invalid path")
        if not path.startswith("/workspace/"):
            raise ValueError("Path must be under /workspace")
        parts = [part for part in path.split("/") if part]
        if ".." in parts:
            raise ValueError("Path traversal is not allowed")
        return path

    def put_file(self, session_id: str, path: str, data: bytes) -> int:
        safe_path = self.validate_workspace_path(path)
        self.files.setdefault(session_id, {})[safe_path] = data
        return len(data)

    def get_file(self, session_id: str, path: str) -> bytes:
        safe_path = self.validate_workspace_path(path)
        return self.files.get(session_id, {})[safe_path]
