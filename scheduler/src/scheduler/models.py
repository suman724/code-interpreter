from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WorkerHeartbeat(BaseModel):
    worker_id: str
    endpoint: str
    cpu_available: int
    memory_available_mib: int
    updated_at: Optional[datetime] = None


class AllocateRequest(BaseModel):
    cpus: int
    memory_mib: int
    disk_mib: int


class AllocateResponse(BaseModel):
    worker_id: str
    endpoint: str
