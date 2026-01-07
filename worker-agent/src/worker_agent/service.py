from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SandboxSession:
    session_id: str
    sandbox_id: str
    workspace_path: str


class MicrosandboxClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def start(self, runtime_image: str) -> str:
        return f"sandbox_{runtime_image.replace('/', '_')}"

    def stop(self, sandbox_id: str) -> None:
        return None

    def run_code(self, sandbox_id: str, code: str, timeout_seconds: int) -> Dict[str, object]:
        return {"stdout": "", "stderr": "", "exit_code": 0}

    def run_command(self, sandbox_id: str, command: str, args: List[str], timeout_seconds: int) -> Dict[str, object]:
        return {"stdout": "", "stderr": "", "exit_code": 0}


class WorkerAgent:
    def __init__(self, microsandbox: MicrosandboxClient, workspace_root: str) -> None:
        self.microsandbox = microsandbox
        self.workspace_root = workspace_root
        self.sessions: Dict[str, SandboxSession] = {}

    def start_session(self, session_id: str, runtime_image: str) -> SandboxSession:
        sandbox_id = self.microsandbox.start(runtime_image)
        workspace_path = f"{self.workspace_root}/{session_id}"
        session = SandboxSession(session_id=session_id, sandbox_id=sandbox_id, workspace_path=workspace_path)
        self.sessions[session_id] = session
        return session

    def stop_session(self, session_id: str) -> None:
        session = self.sessions.pop(session_id)
        self.microsandbox.stop(session.sandbox_id)

    def execute_code(self, session_id: str, code: str, timeout_seconds: int) -> Dict[str, object]:
        session = self.sessions[session_id]
        return self.microsandbox.run_code(session.sandbox_id, code, timeout_seconds)

    def run_command(self, session_id: str, command: str, args: List[str], timeout_seconds: int) -> Dict[str, object]:
        session = self.sessions[session_id]
        return self.microsandbox.run_command(session.sandbox_id, command, args, timeout_seconds)
