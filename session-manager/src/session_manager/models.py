from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class SessionRecord(BaseModel):
    session_id: str
    tenant_id: str
    state: str
    worker_endpoint: Optional[str] = None
    sandbox_id: Optional[str] = None
    created_at: datetime
    expires_at: datetime
    idle_expires_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExecutionRecord(BaseModel):
    execution_id: str
    session_id: str
    status: str
    created_at: datetime
    updated_at: datetime


class IdempotencyRecord(BaseModel):
    idempotency_key: str
    scope: str
    response: Dict[str, Any]
    created_at: datetime
