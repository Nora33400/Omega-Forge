"""Local sandbox execution manager for Omega-Forge.

V1 uses temporary local workspaces and subprocess execution. It is intentionally
simple and CI-friendly. Future versions can add Docker/Moby-backed sessions via
the same high-level concepts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal
import shutil
import subprocess
import tempfile
import time
import uuid

SandboxStatus = Literal["created", "running", "stopped", "destroyed"]
VALID_SANDBOX_STATUSES: set[str] = {"created", "running", "stopped", "destroyed"}


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass
class ExecutionResult:
    """Result of a command executed inside a sandbox session."""

    command: list[str]
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    duration_seconds: float = 0.0
    cwd: str = ""
    timed_out: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.timed_out

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SandboxSession:
    """A local isolated workspace session."""

    workspace_path: str
    status: SandboxStatus = "created"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def mark(self, status: SandboxStatus) -> None:
        if status not in VALID_SANDBOX_STATUSES:
            raise ValueError(f"Invalid sandbox status: {status}")
        self.status = status
        self.updated_at = utc_now()

    @property
    def path(self) -> Path:
        return Path(self.workspace_path)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SandboxManager:
    """Manage temporary local sandbox sessions."""

    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root is not None else Path(tempfile.gettempdir()) / "omega_forge_sandboxes"
        self.root.mkdir(parents=True, exist_ok=True)
        self.sessions: dict[str, SandboxSession] = {}

    def create_session(
        self,
        source_workspace: str | Path | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> SandboxSession:
        session_path = self.root / str(uuid.uuid4())
        session_path.mkdir(parents=True, exist_ok=False)

        if source_workspace is not None:
            self._copy_workspace(Path(source_workspace), session_path)

        session = SandboxSession(
            workspace_path=str(session_path),
            metadata=dict(metadata or {}),
        )
        self.sessions[session.id] = session
        return session

    def run_command(
        self,
        session_id: str,
        command: list[str],
        timeout_seconds: int = 30,
        cwd: str | Path | None = None,
    ) -> ExecutionResult:
        if not command:
            raise ValueError("command cannot be empty")
        session = self.get(session_id)
        if session.status == "destroyed":
            raise RuntimeError("Cannot run command in destroyed sandbox")

        workdir = self._resolve_cwd(session, cwd)
        started = time.monotonic()
        session.mark("running")
        try:
            completed = subprocess.run(
                command,
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )
            duration = time.monotonic() - started
            result = ExecutionResult(
                command=list(command),
                exit_code=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
                duration_seconds=duration,
                cwd=str(workdir),
            )
        except subprocess.TimeoutExpired as exc:
            duration = time.monotonic() - started
            result = ExecutionResult(
                command=list(command),
                exit_code=124,
                stdout=exc.stdout or "",
                stderr=exc.stderr or "",
                duration_seconds=duration,
                cwd=str(workdir),
                timed_out=True,
            )
        finally:
            if session.status != "destroyed":
                session.mark("stopped")
        return result

    def destroy_session(self, session_id: str) -> SandboxSession:
        session = self.get(session_id)
        if session.path.exists():
            shutil.rmtree(session.path)
        session.mark("destroyed")
        return session

    def get(self, session_id: str) -> SandboxSession:
        try:
            return self.sessions[session_id]
        except KeyError as exc:
            raise KeyError(f"Sandbox session not found: {session_id}") from exc

    def list_sessions(self) -> list[SandboxSession]:
        return list(self.sessions.values())

    def _copy_workspace(self, source: Path, target: Path) -> None:
        if not source.exists():
            raise FileNotFoundError(f"Workspace does not exist: {source}")
        if source.is_file():
            shutil.copy2(source, target / source.name)
            return
        for item in source.iterdir():
            destination = target / item.name
            if item.is_dir():
                shutil.copytree(item, destination)
            else:
                shutil.copy2(item, destination)

    def _resolve_cwd(self, session: SandboxSession, cwd: str | Path | None) -> Path:
        base = session.path.resolve()
        if cwd is None:
            return base
        candidate = Path(cwd)
        if not candidate.is_absolute():
            candidate = base / candidate
        resolved = candidate.resolve()
        if base != resolved and base not in resolved.parents:
            raise ValueError("cwd must stay inside the sandbox workspace")
        if not resolved.exists():
            raise FileNotFoundError(f"cwd does not exist: {resolved}")
        return resolved
