from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional

from .models import ExecutionRecord, IdempotencyRecord, SessionRecord


@dataclass
class InMemorySessionStore:
    sessions: Dict[str, SessionRecord] = field(default_factory=dict)
    executions: Dict[str, ExecutionRecord] = field(default_factory=dict)
    idempotency: Dict[str, IdempotencyRecord] = field(default_factory=dict)

    def create_session(self, session: SessionRecord) -> SessionRecord:
        self.sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> SessionRecord:
        return self.sessions[session_id]

    def update_routing(
        self,
        session_id: str,
        worker_endpoint: str,
        sandbox_id: Optional[str] = None,
    ) -> SessionRecord:
        session = self.sessions[session_id]
        session.worker_endpoint = worker_endpoint
        session.sandbox_id = sandbox_id
        self.sessions[session_id] = session
        return session

    def mark_stopped(self, session_id: str) -> None:
        session = self.sessions[session_id]
        session.state = "STOPPED"
        self.sessions[session_id] = session

    def reap_expired(self) -> int:
        now = datetime.utcnow()
        expired = [
            session_id
            for session_id, record in self.sessions.items()
            if record.expires_at <= now or record.idle_expires_at <= now
        ]
        for session_id in expired:
            self.sessions.pop(session_id, None)
        return len(expired)

    def save_idempotency(self, record: IdempotencyRecord) -> None:
        self.idempotency[record.idempotency_key] = record

    def get_idempotency(self, key: str) -> Optional[IdempotencyRecord]:
        return self.idempotency.get(key)

    @staticmethod
    def default_session_timestamps(ttl_seconds: int, idle_seconds: int) -> tuple[datetime, datetime]:
        now = datetime.utcnow()
        return now + timedelta(seconds=ttl_seconds), now + timedelta(seconds=idle_seconds)
