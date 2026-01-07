from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SessionState(str, Enum):
    STARTING = "STARTING"
    READY = "READY"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    ERROR = "ERROR"


class ExecutionStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    TIMEOUT = "TIMEOUT"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class RuntimeSpec(BaseModel):
    language: str
    image: Optional[str] = None
    version: Optional[str] = None


class ResourceLimits(BaseModel):
    cpus: int = Field(default=1, ge=1)
    memory_mib: int = Field(default=512, ge=128)
    disk_mib: int = Field(default=2048, ge=256)


class EgressPolicy(BaseModel):
    mode: str = "deny_all"
    allowlist: List[str] = Field(default_factory=list)


class SessionCreateRequest(BaseModel):
    runtime: RuntimeSpec
    resources: ResourceLimits = Field(default_factory=ResourceLimits)
    egress_policy: EgressPolicy = Field(default_factory=EgressPolicy)
    ttl_seconds: int = Field(default=3600, ge=60)
    idle_timeout_seconds: int = Field(default=900, ge=30)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Session(BaseModel):
    session_id: str
    state: SessionState
    created_at: datetime
    expires_at: datetime
    idle_expires_at: datetime
    runtime: RuntimeSpec
    resources: ResourceLimits
    egress_policy: EgressPolicy


class ExecutionCreateRequest(BaseModel):
    code: str
    timeout_seconds: int = Field(default=30, ge=1, le=600)
    mode: str = "sync"
    capture_paths: List[str] = Field(default_factory=list)
    correlation_id: Optional[str] = None


class CommandRequest(BaseModel):
    command: str
    args: List[str] = Field(default_factory=list)
    timeout_seconds: int = Field(default=30, ge=1, le=600)
    mode: str = "sync"


class Execution(BaseModel):
    execution_id: str
    session_id: str
    status: ExecutionStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    has_error: bool = False
    exit_code: Optional[int] = None
    timing_ms: Dict[str, int] = Field(default_factory=dict)
    artifacts: List[Dict[str, Any]] = Field(default_factory=list)


class FileUploadUrlRequest(BaseModel):
    path: str
    content_type: str
    size_bytes: int = Field(ge=1)


class FileUploadUrlResponse(BaseModel):
    upload_url: str
    object_key: str
    headers: Dict[str, str]


class FileCommitRequest(BaseModel):
    path: str
    object_key: str


class FileDownloadUrlRequest(BaseModel):
    path: str


class FileDownloadUrlResponse(BaseModel):
    download_url: str


class MetricsResponse(BaseModel):
    cpu_usage_percent: float
    memory_usage_mib: float
    disk_usage_bytes: int
    running: bool
