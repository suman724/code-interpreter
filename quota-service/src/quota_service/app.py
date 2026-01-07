from __future__ import annotations

from typing import Dict

from fastapi import FastAPI

from .models import QuotaCheckRequest, QuotaCheckResponse, QuotaRecordRequest
from .store import InMemoryQuotaStore

app = FastAPI(title="Quota Service")
store = InMemoryQuotaStore()


@app.get("/v1/health")
def health() -> Dict[str, bool]:
    return {"ok": True}


@app.post("/v1/quota/check", response_model=QuotaCheckResponse)
def check_quota(payload: QuotaCheckRequest) -> QuotaCheckResponse:
    used = store.get(payload.tenant_id, payload.action)
    remaining = max(payload.limit - used, 0)
    return QuotaCheckResponse(allowed=used < payload.limit, remaining=remaining)


@app.post("/v1/quota/record")
def record_quota(payload: QuotaRecordRequest) -> Dict[str, int]:
    new_value = store.increment(payload.tenant_id, payload.action, payload.amount)
    return {"used": new_value}
