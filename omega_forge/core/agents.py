"""Deterministic agents for Omega-Forge V1.

These agents are intentionally simple. They turn runtime events into new events
and core data structures without requiring an LLM.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from omega_forge.core.agent_message import AgentMessage
from omega_forge.core.forge_runtime import ForgeRuntime


class AgentHandler(Protocol):
    def can_handle(self, message: AgentMessage) -> bool: ...
    def handle(self, runtime: ForgeRuntime, message: AgentMessage) -> list[AgentMessage]: ...


@dataclass
class BaseAgent:
    """Base class for deterministic Omega-Forge agents."""

    name: str
    handled_types: tuple[str, ...]

    def can_handle(self, message: AgentMessage) -> bool:
        return message.message_type in self.handled_types

    def emit(
        self,
        runtime: ForgeRuntime,
        message_type: str,
        payload: dict | None = None,
        receiver: str | None = None,
        correlation_id: str | None = None,
    ) -> AgentMessage:
        return runtime.emit(
            sender=self.name,
            receiver=receiver,
            message_type=message_type,
            payload=dict(payload or {}),
            correlation_id=correlation_id,
        )

    def handle(self, runtime: ForgeRuntime, message: AgentMessage) -> list[AgentMessage]:
        raise NotImplementedError


class PlannerAgent(BaseAgent):
    """Convert a user request into deterministic task proposals."""

    def __init__(self) -> None:
        super().__init__(name="planner", handled_types=("UserRequest",))

    def handle(self, runtime: ForgeRuntime, message: AgentMessage) -> list[AgentMessage]:
        request = str(message.payload.get("request", "")).strip()
        if not request:
            request = "Unspecified request"
        tasks = [
            {"title": "Index workspace", "reason": "Understand available project files"},
            {"title": "Plan implementation", "reason": f"Turn request into steps: {request}"},
            {"title": "Validate result", "reason": "Check output before reporting"},
        ]
        created = self.emit(
            runtime,
            "TasksPlanned",
            payload={"request": request, "tasks": tasks},
            correlation_id=message.id,
        )
        return [created]


class ExecutorAgent(BaseAgent):
    """Execute simple command tasks through ForgeRuntime sandbox execution."""

    def __init__(self) -> None:
        super().__init__(name="executor", handled_types=("ExecuteCommand",))

    def handle(self, runtime: ForgeRuntime, message: AgentMessage) -> list[AgentMessage]:
        raw_command = message.payload.get("command")
        if not isinstance(raw_command, list) or not raw_command:
            failed = self.emit(
                runtime,
                "ExecutionRejected",
                payload={
                    "source_message": message.id,
                    "reason": "payload.command must be a non-empty list",
                },
                correlation_id=message.correlation_id or message.id,
            )
            return [failed]

        command = [str(part) for part in raw_command]
        timeout_seconds = int(message.payload.get("timeout_seconds", 30))
        _session, execution, _report = runtime.run_in_sandbox(
            command,
            timeout_seconds=timeout_seconds,
        )
        completed = self.emit(
            runtime,
            "ExecutionCompleted",
            payload=execution.to_dict(),
            correlation_id=message.correlation_id or message.id,
        )
        return [completed]


class ValidatorAgent(BaseAgent):
    """Validate sandbox execution results."""

    def __init__(self) -> None:
        super().__init__(name="validator", handled_types=("SandboxCommandExecuted", "ExecutionCompleted"))

    def handle(self, runtime: ForgeRuntime, message: AgentMessage) -> list[AgentMessage]:
        exit_code = int(message.payload.get("exit_code", message.payload.get("execution", {}).get("exit_code", 1)))
        if exit_code == 0:
            result = self.emit(
                runtime,
                "ValidationPassed",
                payload={"source_message": message.id, "exit_code": exit_code},
                correlation_id=message.correlation_id or message.id,
            )
            return [result]
        error_text = str(
            message.payload.get("stderr")
            or message.payload.get("execution", {}).get("stderr")
            or f"Command failed with exit code {exit_code}"
        )
        failed = self.emit(
            runtime,
            "ValidationFailed",
            payload={
                "source_message": message.id,
                "exit_code": exit_code,
                "error_text": error_text,
            },
            correlation_id=message.correlation_id or message.id,
        )
        return [failed]


class RepairAgent(BaseAgent):
    """Create failure memory and patch plans from validation failures."""

    def __init__(self) -> None:
        super().__init__(name="repair", handled_types=("ValidationFailed",))

    def handle(self, runtime: ForgeRuntime, message: AgentMessage) -> list[AgentMessage]:
        error_text = str(message.payload.get("error_text", "Unknown validation failure"))
        failure, plan, _report = runtime.record_failure_and_plan(
            error_text=error_text,
            task_title=str(message.payload.get("task_title", "")),
            artifact_path=str(message.payload.get("artifact_path", "")),
            metadata={"source_message": message.id},
        )
        suggested = self.emit(
            runtime,
            "RepairSuggested",
            payload={
                "failure": failure.to_dict(),
                "patch_plan": plan.to_dict(),
            },
            correlation_id=message.correlation_id or message.id,
        )
        return [suggested]


class AgentRegistry:
    """Register agents and dispatch messages to matching handlers."""

    def __init__(self) -> None:
        self.agents: list[AgentHandler] = []

    def register(self, agent: AgentHandler) -> None:
        self.agents.append(agent)

    def dispatch(self, runtime: ForgeRuntime, message: AgentMessage) -> list[AgentMessage]:
        emitted: list[AgentMessage] = []
        for agent in self.agents:
            if agent.can_handle(message):
                emitted.extend(agent.handle(runtime, message))
        return emitted

    def dispatch_history_once(self, runtime: ForgeRuntime) -> list[AgentMessage]:
        emitted: list[AgentMessage] = []
        for message in runtime.bus.history():
            emitted.extend(self.dispatch(runtime, message))
        return emitted
