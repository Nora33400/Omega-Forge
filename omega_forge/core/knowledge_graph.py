"""Knowledge graph primitives for Omega-Forge.

KnowledgeGraph stores typed nodes and directed relations between them. It is a
small dependency-free foundation for future GraphRAG/NetworkX-style reasoning.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
import uuid


@dataclass(frozen=True)
class KnowledgeNode:
    """A typed entity in the Omega-Forge knowledge graph."""

    type: str
    label: str
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.type.strip():
            raise ValueError("node type cannot be empty")
        if not self.label.strip():
            raise ValueError("node label cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "KnowledgeNode":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            type=data["type"],
            label=data["label"],
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass(frozen=True)
class KnowledgeEdge:
    """A directed relation between two knowledge graph nodes."""

    source: str
    target: str
    relation: str
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("edge source cannot be empty")
        if not self.target.strip():
            raise ValueError("edge target cannot be empty")
        if not self.relation.strip():
            raise ValueError("edge relation cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "KnowledgeEdge":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            source=data["source"],
            target=data["target"],
            relation=data["relation"],
            metadata=dict(data.get("metadata") or {}),
        )


class KnowledgeGraph:
    """Small directed typed knowledge graph."""

    def __init__(self) -> None:
        self.nodes: dict[str, KnowledgeNode] = {}
        self.edges: list[KnowledgeEdge] = []

    def add_node(
        self,
        type: str,
        label: str,
        metadata: dict[str, Any] | None = None,
        id: str | None = None,
    ) -> KnowledgeNode:
        node = KnowledgeNode(
            id=id or str(uuid.uuid4()),
            type=type,
            label=label,
            metadata=dict(metadata or {}),
        )
        if node.id in self.nodes:
            raise ValueError(f"Node already exists: {node.id}")
        self.nodes[node.id] = node
        return node

    def add_edge(
        self,
        source: str,
        target: str,
        relation: str,
        metadata: dict[str, Any] | None = None,
        id: str | None = None,
    ) -> KnowledgeEdge:
        if source not in self.nodes:
            raise KeyError(f"Unknown source node: {source}")
        if target not in self.nodes:
            raise KeyError(f"Unknown target node: {target}")
        edge = KnowledgeEdge(
            id=id or str(uuid.uuid4()),
            source=source,
            target=target,
            relation=relation,
            metadata=dict(metadata or {}),
        )
        self.edges.append(edge)
        return edge

    def get_node(self, node_id: str) -> KnowledgeNode:
        try:
            return self.nodes[node_id]
        except KeyError as exc:
            raise KeyError(f"Knowledge node not found: {node_id}") from exc

    def find_nodes(self, type: str | None = None, label_contains: str | None = None) -> list[KnowledgeNode]:
        results = list(self.nodes.values())
        if type is not None:
            results = [node for node in results if node.type == type]
        if label_contains is not None:
            needle = label_contains.lower()
            results = [node for node in results if needle in node.label.lower()]
        return results

    def outgoing(self, node_id: str, relation: str | None = None) -> list[KnowledgeEdge]:
        self.get_node(node_id)
        edges = [edge for edge in self.edges if edge.source == node_id]
        if relation is not None:
            edges = [edge for edge in edges if edge.relation == relation]
        return edges

    def incoming(self, node_id: str, relation: str | None = None) -> list[KnowledgeEdge]:
        self.get_node(node_id)
        edges = [edge for edge in self.edges if edge.target == node_id]
        if relation is not None:
            edges = [edge for edge in edges if edge.relation == relation]
        return edges

    def neighbors(self, node_id: str) -> list[KnowledgeNode]:
        neighbor_ids = {edge.target for edge in self.outgoing(node_id)}
        neighbor_ids.update(edge.source for edge in self.incoming(node_id))
        return [self.nodes[item] for item in sorted(neighbor_ids)]

    def summary(self) -> dict[str, Any]:
        node_types: dict[str, int] = {}
        relations: dict[str, int] = {}
        for node in self.nodes.values():
            node_types[node.type] = node_types.get(node.type, 0) + 1
        for edge in self.edges:
            relations[edge.relation] = relations.get(edge.relation, 0) + 1
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "node_types": dict(sorted(node_types.items())),
            "relations": dict(sorted(relations.items())),
        }

    def export(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges],
        }

    @classmethod
    def from_export(cls, payload: dict[str, Any]) -> "KnowledgeGraph":
        graph = cls()
        for raw_node in payload.get("nodes", []):
            node = KnowledgeNode.from_dict(raw_node)
            graph.nodes[node.id] = node
        for raw_edge in payload.get("edges", []):
            edge = KnowledgeEdge.from_dict(raw_edge)
            if edge.source not in graph.nodes or edge.target not in graph.nodes:
                raise ValueError("edge references unknown node")
            graph.edges.append(edge)
        return graph
