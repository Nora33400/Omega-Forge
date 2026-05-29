"""Project state persistence for Omega-Forge."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class StateEvent:
    timestamp: str
    message: str


@dataclass
class ProjectStateData:
    version: str = "0.1.0"
    goal: str = "Build Omega-Forge"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    completed_tasks: int = 0
    failed_tasks: int = 0
    reports: list[str] = field(default_factory=list)
    history: list[StateEvent] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectStateData":
        history = [StateEvent(**item) for item in data.get("history", [])]
        return cls(
            version=data.get("version", "0.1.0"),
            goal=data.get("goal", "Build Omega-Forge"),
            created_at=data.get("created_at", utc_now()),
            updated_at=data.get("updated_at", utc_now()),
            completed_tasks=int(data.get("completed_tasks", 0)),
            failed_tasks=int(data.get("failed_tasks", 0)),
            reports=list(data.get("reports", [])),
            history=history,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ProjectState:
    """Persistent global state of an Omega-Forge workspace."""

    def __init__(self, path: str | Path = "omega_forge_state.json") -> None:
        self.path = Path(path)
        self.data = ProjectStateData()
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid project state JSON: {self.path}") from exc
        self.data = ProjectStateData.from_dict(payload)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data.updated_at = utc_now()
        self.path.write_text(
            json.dumps(self.data.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def add_event(self, message: str) -> None:
        now = utc_now()
        self.data.updated_at = now
        self.data.history.append(StateEvent(timestamp=now, message=message))
        self.save()

    def set_goal(self, goal: str) -> None:
        if not goal.strip():
            raise ValueError("Goal cannot be empty")
        self.data.goal = goal.strip()
        self.add_event(f"Goal updated: {self.data.goal}")

    def record_completed_task(self) -> None:
        self.data.completed_tasks += 1
        self.add_event("Completed task recorded")

    def record_failed_task(self) -> None:
        self.data.failed_tasks += 1
        self.add_event("Failed task recorded")

    def add_report(self, report_path: str | Path) -> None:
        report = str(report_path)
        self.data.reports.append(report)
        self.add_event(f"Report added: {report}")

    def summary(self) -> dict[str, Any]:
        return {
            "version": self.data.version,
            "goal": self.data.goal,
            "completed_tasks": self.data.completed_tasks,
            "failed_tasks": self.data.failed_tasks,
            "reports": len(self.data.reports),
            "history_events": len(self.data.history),
            "updated_at": self.data.updated_at,
        }
