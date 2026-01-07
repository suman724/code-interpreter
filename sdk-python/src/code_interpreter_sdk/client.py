from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class ClientConfig:
    base_url: str
    token: str


class CodeInterpreterClient:
    def __init__(self, config: ClientConfig) -> None:
        self.config = config

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.config.token}"}

    def create_session(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.config.base_url}/v1/sessions",
            json=payload,
            headers=self._headers(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def run_code(self, session_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.config.base_url}/v1/sessions/{session_id}/executions",
            json=payload,
            headers=self._headers(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def upload_url(self, session_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.config.base_url}/v1/sessions/{session_id}/files:upload-url",
            json=payload,
            headers=self._headers(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def download_url(self, session_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.config.base_url}/v1/sessions/{session_id}/files:download-url",
            json=payload,
            headers=self._headers(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def upload_file(self, session_id: str, path: str, data: bytes) -> Dict[str, Any]:
        response = requests.put(
            f"{self.config.base_url}/v1/sessions/{session_id}/files/{path.lstrip('/')}",
            data=data,
            headers=self._headers(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def download_file(self, session_id: str, path: str) -> bytes:
        response = requests.get(
            f"{self.config.base_url}/v1/sessions/{session_id}/files/{path.lstrip('/')}",
            headers=self._headers(),
            timeout=30,
        )
        response.raise_for_status()
        return response.content

    def close_session(self, session_id: str) -> None:
        response = requests.delete(
            f"{self.config.base_url}/v1/sessions/{session_id}",
            headers=self._headers(),
            timeout=30,
        )
        response.raise_for_status()
