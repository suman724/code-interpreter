from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, Tuple


@dataclass
class InMemoryQuotaStore:
    counters: DefaultDict[Tuple[str, str], int] = field(default_factory=lambda: defaultdict(int))

    def increment(self, tenant_id: str, action: str, amount: int) -> int:
        key = (tenant_id, action)
        self.counters[key] += amount
        return self.counters[key]

    def get(self, tenant_id: str, action: str) -> int:
        return self.counters[(tenant_id, action)]
