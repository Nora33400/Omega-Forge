"""Base agent abstractions for Omega-Forge."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import uuid


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class AgentResult:
    """Result returned by an agent run."""

    agent_name: str
    success: bool
    message: str
    data: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=utc_now)


class BaseAgent:
    """Small deterministic base class for Omega-Forge agents."""

    name = "base"
    role = "generic"

    def describe(self) -> dict[str, str]:
        return {"name": self.name, "role": self.role}

    def run(self, context: dict[str, Any]) -> AgentResult:
        raise NotImplementedError("Agents must implement run(context).")

    def ok(self, message: str, data: dict[str, Any] | None = None) -> AgentResult:
        return AgentResult(
            agent_name=self.name,
            success=True,
            message=message,
            data=data or {},
        )

    def fail(self, message: str, data: dict[str, Any] | None = None) -> AgentResult:
        return AgentResult(
            agent_name=self.name,
            success=False,
            message=message,
            data=data or {},
        )
