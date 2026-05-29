"""JSON-backed task queue for Omega-Forge.

The queue is intentionally small and deterministic in V0.
It stores every task in a single JSON file so the project can resume after interruption.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Literal
import json
import uuid

TaskStatus = Literal["pending", "running", "done", "failed", "blocked"]

VALID_STATUSES: set[str] = {"pending", "running", "done", "failed", "blocked"}


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass
class TaskEvent:
    """A state transition or note attached to a task."""

    timestamp: str
    message: str


@dataclass
class Task:
    """A single Omega-Forge task."""

    title: str
    description: str = ""
    priority: int = 3
    status: TaskStatus = "pending"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    history: list[TaskEvent] = field(default_factory=list)

    def add_event(self, message: str) -> None:
        self.updated_at = utc_now()
        self.history.append(TaskEvent(timestamp=self.updated_at, message=message))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        history = [TaskEvent(**item) for item in data.get("history", [])]
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            priority=int(data.get("priority", 3)),
            status=data.get("status", "pending"),
            created_at=data.get("created_at", utc_now()),
            updated_at=data.get("updated_at", utc_now()),
            history=history,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TaskQueue:
    """Persistent task queue stored as JSON."""

    def __init__(self, path: str | Path = "omega_forge_tasks.json") -> None:
        self.path = Path(path)
        self.tasks: list[Task] = []
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            self.tasks = []
            return

        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid task queue JSON: {self.path}") from exc

        raw_tasks = payload.get("tasks", payload if isinstance(payload, list) else [])
        self.tasks = [Task.from_dict(item) for item in raw_tasks]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"tasks": [task.to_dict() for task in self.tasks]}
        self.path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def add(self, title: str, description: str = "", priority: int = 3) -> Task:
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        task = Task(title=title.strip(), description=description.strip(), priority=priority)
        task.add_event("Task created")
        self.tasks.append(task)
        self.save()
        return task

    def list(self, status: str | None = None) -> list[Task]:
        if status is None:
            return list(self.tasks)
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid task status: {status}")
        return [task for task in self.tasks if task.status == status]

    def get(self, task_id: str) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"Task not found: {task_id}")

    def set_status(self, task_id: str, status: TaskStatus, note: str | None = None) -> Task:
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid task status: {status}")
        task = self.get(task_id)
        old_status = task.status
        task.status = status
        message = note or f"Status changed from {old_status} to {status}"
        task.add_event(message)
        self.save()
        return task

    def pending(self) -> list[Task]:
        return self.list("pending")

    def summary(self) -> dict[str, int]:
        counts = {status: 0 for status in VALID_STATUSES}
        for task in self.tasks:
            counts[task.status] = counts.get(task.status, 0) + 1
        counts["total"] = len(self.tasks)
        return counts

    def extend(self, tasks: Iterable[Task]) -> None:
        self.tasks.extend(tasks)
        self.save()
