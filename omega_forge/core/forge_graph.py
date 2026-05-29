"""Deterministic execution graph for Omega-Forge.

ForgeGraph is intentionally small in V1. It provides enough structure to model
agent/workflow routing without pulling in a heavy orchestration framework.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Callable

ForgeNodeHandler = Callable[[dict[str, Any]], dict[str, Any] | None]
ForgeCondition = Callable[[dict[str, Any]], bool]


@dataclass(frozen=True)
class ForgeNode:
    """A named graph node."""

    name: str
    description: str = ""


@dataclass(frozen=True)
class ForgeEdge:
    """A directed graph edge between nodes."""

    source: str
    target: str
    label: str = ""
    condition_name: str | None = None


@dataclass
class ForgeGraphRun:
    """Result of a ForgeGraph execution."""

    start: str
    state: dict[str, Any]
    path: list[str] = field(default_factory=list)
    transitions: list[dict[str, Any]] = field(default_factory=list)
    stopped_reason: str = "completed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ForgeGraph:
    """Small directed execution graph with optional conditional edges."""

    def __init__(self) -> None:
        self.nodes: dict[str, ForgeNode] = {}
        self.edges: list[ForgeEdge] = []
        self._handlers: dict[str, ForgeNodeHandler] = {}
        self._conditions: dict[str, ForgeCondition] = {}

    def add_node(
        self,
        name: str,
        handler: ForgeNodeHandler | None = None,
        description: str = "",
    ) -> "ForgeGraph":
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Node name cannot be empty")
        if clean_name in self.nodes:
            raise ValueError(f"Node already exists: {clean_name}")
        self.nodes[clean_name] = ForgeNode(name=clean_name, description=description.strip())
        if handler is not None:
            self._handlers[clean_name] = handler
        return self

    def add_edge(
        self,
        source: str,
        target: str,
        label: str = "",
        condition_name: str | None = None,
        condition: ForgeCondition | None = None,
    ) -> "ForgeGraph":
        self._require_node(source)
        self._require_node(target)
        if condition is not None:
            if not condition_name:
                raise ValueError("condition_name is required when condition is provided")
            self._conditions[condition_name] = condition
        elif condition_name and condition_name not in self._conditions:
            raise ValueError(f"Unknown condition: {condition_name}")
        self.edges.append(
            ForgeEdge(
                source=source,
                target=target,
                label=label.strip(),
                condition_name=condition_name,
            )
        )
        return self

    def add_condition(self, name: str, condition: ForgeCondition) -> "ForgeGraph":
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Condition name cannot be empty")
        self._conditions[clean_name] = condition
        return self

    def run(
        self,
        start: str,
        state: dict[str, Any] | None = None,
        max_steps: int = 100,
    ) -> ForgeGraphRun:
        self._require_node(start)
        if max_steps <= 0:
            raise ValueError("max_steps must be positive")

        current = start
        run_state: dict[str, Any] = dict(state or {})
        result = ForgeGraphRun(start=start, state=run_state)

        for _ in range(max_steps):
            result.path.append(current)
            handler = self._handlers.get(current)
            if handler is not None:
                update = handler(run_state)
                if update:
                    run_state.update(update)

            next_edge = self._select_edge(current, run_state)
            if next_edge is None:
                result.stopped_reason = "no_next_edge"
                return result

            result.transitions.append(
                {
                    "source": next_edge.source,
                    "target": next_edge.target,
                    "label": next_edge.label,
                    "condition_name": next_edge.condition_name,
                }
            )
            current = next_edge.target

        result.stopped_reason = "max_steps_reached"
        return result

    def export(self) -> dict[str, Any]:
        """Export a frontend-agnostic graph representation."""

        return {
            "nodes": [asdict(node) for node in self.nodes.values()],
            "edges": [asdict(edge) for edge in self.edges],
        }

    def _select_edge(self, source: str, state: dict[str, Any]) -> ForgeEdge | None:
        candidates = [edge for edge in self.edges if edge.source == source]
        for edge in candidates:
            if edge.condition_name is None:
                return edge
            condition = self._conditions[edge.condition_name]
            if condition(state):
                return edge
        return None

    def _require_node(self, name: str) -> None:
        if name not in self.nodes:
            raise KeyError(f"Unknown node: {name}")
