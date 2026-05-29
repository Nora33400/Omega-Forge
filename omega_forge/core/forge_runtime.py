"""Runtime assembly layer for Omega-Forge.

ForgeRuntime wires the core primitives together without hiding them. It is the
first place where indexing, graphing, event messages, failure memory, patch
planning, and sandbox execution begin to act as a coherent system.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from omega_forge.core.agent_bus import AgentBus
from omega_forge.core.agent_message import AgentMessage
from omega_forge.core.failure_memory import FailureMemory, FailureMemoryEntry
from omega_forge.core.forge_graph import ForgeGraph
from omega_forge.core.knowledge_graph import KnowledgeGraph
from omega_forge.core.patch_plan import PatchPlan, build_patch_plan_from_failure
from omega_forge.core.project_index import ProjectIndex
from omega_forge.core.sandbox_manager import ExecutionResult, SandboxManager, SandboxSession


@dataclass
class RuntimeReport:
    """A serializable report produced by ForgeRuntime operations."""

    operation: str
    ok: bool = True
    data: dict[str, Any] = field(default_factory=dict)
    messages: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ForgeRuntime:
    """Coordinate the Omega-Forge core components."""

    def __init__(
        self,
        workspace: str | Path,
        failure_memory_path: str | Path | None = None,
        sandbox_root: str | Path | None = None,
    ) -> None:
        self.workspace = Path(workspace).resolve()
        if not self.workspace.exists():
            raise FileNotFoundError(f"Workspace does not exist: {self.workspace}")
        if not self.workspace.is_dir():
            raise NotADirectoryError(f"Workspace is not a directory: {self.workspace}")

        self.bus = AgentBus()
        self.flow = ForgeGraph()
        self.knowledge = KnowledgeGraph()
        self.index = ProjectIndex(self.workspace)
        self.failure_memory = FailureMemory(
            failure_memory_path or self.workspace / ".omega_forge_failures.json"
        )
        self.sandbox = SandboxManager(sandbox_root)

    def emit(
        self,
        sender: str,
        message_type: str,
        payload: dict[str, Any] | None = None,
        receiver: str | None = None,
        correlation_id: str | None = None,
    ) -> AgentMessage:
        message = AgentMessage(
            sender=sender,
            receiver=receiver,
            message_type=message_type,
            payload=dict(payload or {}),
            correlation_id=correlation_id,
        )
        self.bus.publish(message)
        return message

    def index_workspace(self) -> RuntimeReport:
        self.index.build()
        project_node = self.knowledge.add_node(
            "Project",
            self.workspace.name,
            metadata={"path": str(self.workspace)},
        )
        for file in self.index.files:
            file_node = self.knowledge.add_node(
                "File",
                file.path,
                metadata={
                    "extension": file.extension,
                    "size_bytes": file.size_bytes,
                    "line_count": file.line_count,
                },
            )
            self.knowledge.add_edge(project_node.id, file_node.id, "contains")

        self.emit(
            "runtime",
            "WorkspaceIndexed",
            payload=self.index.summary(),
        )
        return self._report(
            "index_workspace",
            data={
                "index": self.index.summary(),
                "knowledge": self.knowledge.summary(),
            },
        )

    def record_failure_and_plan(
        self,
        error_text: str,
        task_title: str = "",
        project_type: str = "",
        template_name: str = "",
        artifact_path: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> tuple[FailureMemoryEntry, PatchPlan, RuntimeReport]:
        failure = self.failure_memory.record_failure(
            error_text=error_text,
            task_title=task_title,
            project_type=project_type,
            template_name=template_name,
            artifact_path=artifact_path,
            metadata=dict(metadata or {}),
        )
        plan = build_patch_plan_from_failure(
            failure_id=failure.id,
            error_text=error_text,
            artifact_path=artifact_path,
            metadata={"failure_signature": failure.signature},
        )

        failure_node = self.knowledge.add_node(
            "Failure",
            failure.signature,
            metadata=failure.to_dict(),
        )
        patch_node = self.knowledge.add_node(
            "PatchPlan",
            plan.strategy,
            metadata=plan.to_dict(),
        )
        self.knowledge.add_edge(failure_node.id, patch_node.id, "planned_repair")

        self.emit(
            "runtime",
            "FailureRecorded",
            payload=failure.to_dict(),
        )
        self.emit(
            "runtime",
            "PatchPlanCreated",
            payload=plan.to_dict(),
            correlation_id=failure.id,
        )

        report = self._report(
            "record_failure_and_plan",
            data={
                "failure": failure.to_dict(),
                "patch_plan": plan.to_dict(),
                "knowledge": self.knowledge.summary(),
            },
        )
        return failure, plan, report

    def run_in_sandbox(
        self,
        command: list[str],
        timeout_seconds: int = 30,
    ) -> tuple[SandboxSession, ExecutionResult, RuntimeReport]:
        session = self.sandbox.create_session(source_workspace=self.workspace)
        self.emit(
            "runtime",
            "SandboxSessionCreated",
            payload=session.to_dict(),
        )
        result = self.sandbox.run_command(
            session.id,
            command,
            timeout_seconds=timeout_seconds,
        )
        self.emit(
            "runtime",
            "SandboxCommandExecuted",
            payload=result.to_dict(),
            correlation_id=session.id,
        )
        report = self._report(
            "run_in_sandbox",
            ok=result.ok,
            data={
                "session": session.to_dict(),
                "execution": result.to_dict(),
            },
        )
        self.sandbox.destroy_session(session.id)
        return session, result, report

    def _report(self, operation: str, ok: bool = True, data: dict[str, Any] | None = None) -> RuntimeReport:
        return RuntimeReport(
            operation=operation,
            ok=ok,
            data=dict(data or {}),
            messages=[message.to_dict() for message in self.bus.history()],
        )
