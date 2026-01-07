from __future__ import annotations

from pydantic import BaseModel


class QuotaCheckRequest(BaseModel):
    tenant_id: str
    action: str
    limit: int
    window_seconds: int


class QuotaCheckResponse(BaseModel):
    allowed: bool
    remaining: int


class QuotaRecordRequest(BaseModel):
    tenant_id: str
    action: str
    amount: int = 1
