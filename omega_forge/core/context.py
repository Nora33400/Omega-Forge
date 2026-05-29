"""Workspace context builder for Omega-Forge.

The context builder summarizes the current project layout so agents and
artifact templates can make decisions from observable repository state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path

from omega_forge.core.task_queue import TaskQueue


@dataclass(frozen=True)
class WorkspaceContext:
    root: str
    project_type: str
    has_docs: bool
    has_tests: bool
    has_core: bool
    has_agents: bool
    python_files: list[str] = field(default_factory=list)
    markdown_files: list[str] = field(default_factory=list)
    pending_tasks: list[str] = field(default_factory=list)
    done_tasks: list[str] = field(default_factory=list)
    blocked_tasks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class ContextBuilder:
    """Build a compact deterministic context snapshot for a workspace."""

    def __init__(self, root: str | Path = ".", queue_path: str | Path | None = None) -> None:
        self.root = Path(root)
        self.queue_path = Path(queue_path) if queue_path else self.root / "omega_forge_tasks.json"

    def build(self) -> WorkspaceContext:
        queue = TaskQueue(self.queue_path)
        python_files = self._relative_files("*.py")
        markdown_files = self._relative_files("*.md")

        return WorkspaceContext(
            root=str(self.root),
            project_type=self._detect_project_type(python_files),
            has_docs=(self.root / "docs").exists(),
            has_tests=(self.root / "tests").exists(),
            has_core=(self.root / "omega_forge" / "core").exists(),
            has_agents=(self.root / "omega_forge" / "agents").exists(),
            python_files=python_files,
            markdown_files=markdown_files,
            pending_tasks=[task.title for task in queue.list("pending")],
            done_tasks=[task.title for task in queue.list("done")],
            blocked_tasks=[task.title for task in queue.list("blocked")],
        )

    def _relative_files(self, pattern: str) -> list[str]:
        if not self.root.exists():
            return []
        ignored_parts = {".git", "__pycache__", ".pytest_cache", ".venv", "venv"}
        files = []
        for path in self.root.rglob(pattern):
            if any(part in ignored_parts for part in path.parts):
                continue
            if path.is_file():
                files.append(path.relative_to(self.root).as_posix())
        return sorted(files)

    @staticmethod
    def _detect_project_type(python_files: list[str]) -> str:
        if any(path.startswith("omega_forge/") for path in python_files):
            return "python_package"
        if python_files:
            return "python_project"
        return "generic_workspace"
