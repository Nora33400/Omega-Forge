"""Patch planning primitives for Omega-Forge.

PatchPlan does not apply edits by itself. It describes what should be repaired,
why, and where, so future PatchApplier and SandboxManager layers can execute
plans safely and audibly.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal
import uuid

PatchStrategy = Literal[
    "add_dependency",
    "create_missing_file",
    "create_missing_symbol",
    "fix_import",
    "fix_path",
    "repair_configuration",
    "retry_generation",
    "manual_review",
]

PatchPlanStatus = Literal["pending", "approved", "applied", "rejected", "failed"]

VALID_PATCH_STRATEGIES: set[str] = {
    "add_dependency",
    "create_missing_file",
    "create_missing_symbol",
    "fix_import",
    "fix_path",
    "repair_configuration",
    "retry_generation",
    "manual_review",
}

VALID_PATCH_STATUSES: set[str] = {"pending", "approved", "applied", "rejected", "failed"}


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass
class PatchTarget:
    """A file or logical location targeted by a patch plan."""

    path: str
    reason: str = ""
    must_exist: bool = False

    def __post_init__(self) -> None:
        if not self.path.strip():
            raise ValueError("Patch target path cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PatchTarget":
        return cls(
            path=data["path"],
            reason=data.get("reason", ""),
            must_exist=bool(data.get("must_exist", False)),
        )


@dataclass
class PatchPlan:
    """A safe, reviewable plan for repairing a known failure."""

    strategy: PatchStrategy
    rationale: str
    targets: list[PatchTarget] = field(default_factory=list)
    failure_id: str | None = None
    status: PatchPlanStatus = "pending"
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if self.strategy not in VALID_PATCH_STRATEGIES:
            raise ValueError(f"Invalid patch strategy: {self.strategy}")
        if self.status not in VALID_PATCH_STATUSES:
            raise ValueError(f"Invalid patch status: {self.status}")
        if not self.rationale.strip():
            raise ValueError("Patch rationale cannot be empty")

    def mark(self, status: PatchPlanStatus) -> None:
        if status not in VALID_PATCH_STATUSES:
            raise ValueError(f"Invalid patch status: {status}")
        self.status = status
        self.updated_at = utc_now()

    def add_target(self, path: str, reason: str = "", must_exist: bool = False) -> PatchTarget:
        target = PatchTarget(path=path, reason=reason, must_exist=must_exist)
        self.targets.append(target)
        self.updated_at = utc_now()
        return target

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["targets"] = [target.to_dict() for target in self.targets]
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PatchPlan":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            created_at=data.get("created_at", utc_now()),
            updated_at=data.get("updated_at", utc_now()),
            failure_id=data.get("failure_id"),
            strategy=data["strategy"],
            rationale=data["rationale"],
            targets=[PatchTarget.from_dict(item) for item in data.get("targets", [])],
            status=data.get("status", "pending"),
            metadata=dict(data.get("metadata") or {}),
        )


def infer_patch_strategy(error_text: str) -> PatchStrategy:
    """Infer a conservative repair strategy from common error text."""

    normalized = error_text.lower()
    if "modulenotfounderror" in normalized or "no module named" in normalized:
        return "add_dependency"
    if "filenotfounderror" in normalized or "no such file" in normalized:
        return "create_missing_file"
    if "nameerror" in normalized or "is not defined" in normalized:
        return "create_missing_symbol"
    if "importerror" in normalized or "cannot import" in normalized:
        return "fix_import"
    if "path" in normalized and ("not found" in normalized or "invalid" in normalized):
        return "fix_path"
    if "config" in normalized or "configuration" in normalized:
        return "repair_configuration"
    if "timeout" in normalized or "temporary" in normalized:
        return "retry_generation"
    return "manual_review"


def build_patch_plan_from_failure(
    failure_id: str,
    error_text: str,
    artifact_path: str = "",
    metadata: dict[str, Any] | None = None,
) -> PatchPlan:
    """Create a conservative PatchPlan from a failure record."""

    strategy = infer_patch_strategy(error_text)
    plan = PatchPlan(
        failure_id=failure_id,
        strategy=strategy,
        rationale=f"Repair strategy inferred from failure: {error_text[:160]}",
        metadata=dict(metadata or {}),
    )
    if artifact_path:
        plan.add_target(
            artifact_path,
            reason="Artifact associated with the recorded failure",
            must_exist=False,
        )
    return plan
