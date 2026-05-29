"""JSON-backed failure memory for Omega-Forge.

FailureMemory stores validation errors, repair attempts, and outcomes so the
forge can detect repeated failures and eventually learn from successful repairs.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Literal
import json
import uuid

FailureStatus = Literal["unresolved", "resolved", "repeated", "ignored"]
VALID_FAILURE_STATUSES: set[str] = {"unresolved", "resolved", "repeated", "ignored"}


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


def error_signature(error_text: str, template_name: str = "", project_type: str = "") -> str:
    """Create a stable short signature for a failure."""

    normalized = "\n".join(
        part.strip().lower()
        for part in [project_type, template_name, error_text]
        if part and part.strip()
    )
    return sha256(normalized.encode("utf-8")).hexdigest()[:16]


@dataclass
class FailureMemoryEntry:
    """A recorded generation, validation, or repair failure."""

    error_text: str
    task_title: str = ""
    project_type: str = ""
    template_name: str = ""
    artifact_path: str = ""
    repair_task: str = ""
    repair_result: str = ""
    status: FailureStatus = "unresolved"
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    signature: str = ""

    def __post_init__(self) -> None:
        if not self.error_text.strip():
            raise ValueError("error_text cannot be empty")
        if self.status not in VALID_FAILURE_STATUSES:
            raise ValueError(f"Invalid failure status: {self.status}")
        if not self.signature:
            self.signature = error_signature(
                self.error_text,
                template_name=self.template_name,
                project_type=self.project_type,
            )

    def mark(self, status: FailureStatus, repair_result: str = "") -> None:
        if status not in VALID_FAILURE_STATUSES:
            raise ValueError(f"Invalid failure status: {status}")
        self.status = status
        if repair_result:
            self.repair_result = repair_result
        self.updated_at = utc_now()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FailureMemoryEntry":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            created_at=data.get("created_at", utc_now()),
            updated_at=data.get("updated_at", utc_now()),
            error_text=data["error_text"],
            task_title=data.get("task_title", ""),
            project_type=data.get("project_type", ""),
            template_name=data.get("template_name", ""),
            artifact_path=data.get("artifact_path", ""),
            repair_task=data.get("repair_task", ""),
            repair_result=data.get("repair_result", ""),
            status=data.get("status", "unresolved"),
            metadata=dict(data.get("metadata") or {}),
            signature=data.get("signature", ""),
        )


class FailureMemory:
    """Persistent local failure memory stored as JSON."""

    def __init__(self, path: str | Path = "omega_forge_failures.json") -> None:
        self.path = Path(path)
        self.entries: list[FailureMemoryEntry] = []
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            self.entries = []
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid failure memory JSON: {self.path}") from exc
        raw_entries = payload.get("failures", payload if isinstance(payload, list) else [])
        self.entries = [FailureMemoryEntry.from_dict(item) for item in raw_entries]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"failures": [entry.to_dict() for entry in self.entries]}
        self.path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def add(self, entry: FailureMemoryEntry) -> FailureMemoryEntry:
        existing = self.find_by_signature(entry.signature)
        if existing:
            existing.mark("repeated")
            self.save()
            return existing
        self.entries.append(entry)
        self.save()
        return entry

    def record_failure(
        self,
        error_text: str,
        task_title: str = "",
        project_type: str = "",
        template_name: str = "",
        artifact_path: str = "",
        repair_task: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> FailureMemoryEntry:
        entry = FailureMemoryEntry(
            error_text=error_text,
            task_title=task_title,
            project_type=project_type,
            template_name=template_name,
            artifact_path=artifact_path,
            repair_task=repair_task,
            metadata=dict(metadata or {}),
        )
        return self.add(entry)

    def find_by_signature(self, signature: str) -> FailureMemoryEntry | None:
        for entry in self.entries:
            if entry.signature == signature:
                return entry
        return None

    def find_similar(
        self,
        error_text: str,
        template_name: str = "",
        project_type: str = "",
    ) -> FailureMemoryEntry | None:
        signature = error_signature(error_text, template_name=template_name, project_type=project_type)
        return self.find_by_signature(signature)

    def mark_resolved(self, entry_id: str, repair_result: str = "") -> FailureMemoryEntry:
        entry = self.get(entry_id)
        entry.mark("resolved", repair_result=repair_result)
        self.save()
        return entry

    def mark_ignored(self, entry_id: str) -> FailureMemoryEntry:
        entry = self.get(entry_id)
        entry.mark("ignored")
        self.save()
        return entry

    def get(self, entry_id: str) -> FailureMemoryEntry:
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        raise KeyError(f"Failure memory entry not found: {entry_id}")

    def list(self, status: FailureStatus | None = None) -> list[FailureMemoryEntry]:
        if status is None:
            return list(self.entries)
        if status not in VALID_FAILURE_STATUSES:
            raise ValueError(f"Invalid failure status: {status}")
        return [entry for entry in self.entries if entry.status == status]

    def summary(self) -> dict[str, int]:
        counts = {status: 0 for status in VALID_FAILURE_STATUSES}
        for entry in self.entries:
            counts[entry.status] = counts.get(entry.status, 0) + 1
        counts["total"] = len(self.entries)
        return counts
