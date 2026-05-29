"""Agent messages for Omega-Forge.

The message model is deliberately small and serializable so it can be logged,
replayed, persisted, and later connected to a richer agent bus.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import uuid


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class AgentMessage:
    """A message exchanged between Omega-Forge agents."""

    sender: str
    message_type: str
    payload: dict[str, Any] = field(default_factory=dict)
    receiver: str | None = None
    correlation_id: str | None = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.sender.strip():
            raise ValueError("sender cannot be empty")
        if not self.message_type.strip():
            raise ValueError("message_type cannot be empty")
        if self.receiver is not None and not self.receiver.strip():
            raise ValueError("receiver cannot be blank when provided")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentMessage":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            sender=data["sender"],
            receiver=data.get("receiver"),
            message_type=data["message_type"],
            payload=dict(data.get("payload") or {}),
            correlation_id=data.get("correlation_id"),
            timestamp=data.get("timestamp", utc_now()),
        )
