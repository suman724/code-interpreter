from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from .models import AllocateRequest, AllocateResponse, WorkerHeartbeat


@dataclass
class WorkerStore:
    workers: Dict[str, WorkerHeartbeat] = field(default_factory=dict)

    def record_heartbeat(self, heartbeat: WorkerHeartbeat) -> WorkerHeartbeat:
        self.workers[heartbeat.worker_id] = heartbeat
        return heartbeat

    def allocate(self, request: AllocateRequest) -> Optional[AllocateResponse]:
        for worker in self.workers.values():
            if worker.cpu_available >= request.cpus and worker.memory_available_mib >= request.memory_mib:
                return AllocateResponse(worker_id=worker.worker_id, endpoint=worker.endpoint)
        return None
