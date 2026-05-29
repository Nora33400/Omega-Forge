"""Deterministic in-process agent event bus for Omega-Forge."""

from __future__ import annotations

from collections import defaultdict
from typing import Callable

from omega_forge.core.agent_message import AgentMessage

MessageHandler = Callable[[AgentMessage], None]


class AgentBus:
    """Simple publish/subscribe bus with message history."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[MessageHandler]] = defaultdict(list)
        self._history: list[AgentMessage] = []

    def subscribe(self, message_type: str, handler: MessageHandler) -> None:
        if not message_type.strip():
            raise ValueError("message_type cannot be empty")
        self._subscribers[message_type].append(handler)

    def publish(self, message: AgentMessage) -> None:
        self._history.append(message)
        for handler in self._subscribers.get(message.message_type, []):
            handler(message)

    def send(self, message: AgentMessage) -> None:
        self.publish(message)

    def history(self) -> list[AgentMessage]:
        return list(self._history)

    def count(self) -> int:
        return len(self._history)

    def clear(self) -> None:
        self._history.clear()
