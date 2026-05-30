"""End-to-end deterministic execution loop for Omega-Forge."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from omega_forge.core.agent_message import AgentMessage
from omega_forge.core.agents import (
    AgentRegistry,
    ExecutorAgent,
    PlannerAgent,
    RepairAgent,
    ValidatorAgent,
)
from omega_forge.core.forge_runtime import ForgeRuntime


@dataclass
class ExecutionLoopResult:
    """Serializable result of one ExecutionLoop run."""

    request: str
    ok: bool
    tasks: list[dict[str, Any]] = field(default_factory=list)
    execution: dict[str, Any] | None = None
    validation: dict[str, Any] | None = None
    repair: dict[str, Any] | None = None
    emitted_messages: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ExecutionLoop:
    """Coordinate Planner, Executor, Validator, and Repair agents."""

    def __init__(self) -> None:
        self.registry = AgentRegistry()
        self.registry.register(PlannerAgent())
        self.registry.register(ExecutorAgent())
        self.registry.register(ValidatorAgent())
        self.registry.register(RepairAgent())

    def run(
        self,
        runtime: ForgeRuntime,
        request: str,
        command: list[str],
        timeout_seconds: int = 30,
    ) -> ExecutionLoopResult:
        emitted: list[AgentMessage] = []

        user_request = runtime.emit(
            "user",
            "UserRequest",
            payload={"request": request},
        )
        emitted.append(user_request)

        planned = self.registry.dispatch(runtime, user_request)
        emitted.extend(planned)
        tasks = self._tasks_from(planned)

        execute_command = runtime.emit(
            "execution_loop",
            "ExecuteCommand",
            payload={
                "command": list(command),
                "timeout_seconds": timeout_seconds,
                "request": request,
            },
            correlation_id=user_request.id,
        )
        emitted.append(execute_command)

        execution_messages = self.registry.dispatch(runtime, execute_command)
        emitted.extend(execution_messages)
        execution_message = self._latest_of_type(
            execution_messages,
            ("ExecutionCompleted", "ExecutionRejected"),
        )

        if execution_message is None or execution_message.message_type == "ExecutionRejected":
            return ExecutionLoopResult(
                request=request,
                ok=False,
                tasks=tasks,
                execution=execution_message.to_dict() if execution_message else None,
                emitted_messages=[message.to_dict() for message in emitted],
            )

        validation_messages = self.registry.dispatch(runtime, execution_message)
        emitted.extend(validation_messages)
        validation_message = self._latest_of_type(
            validation_messages,
            ("ValidationPassed", "ValidationFailed"),
        )

        if validation_message is None:
            return ExecutionLoopResult(
                request=request,
                ok=False,
                tasks=tasks,
                execution=execution_message.to_dict(),
                emitted_messages=[message.to_dict() for message in emitted],
            )

        if validation_message.message_type == "ValidationPassed":
            return ExecutionLoopResult(
                request=request,
                ok=True,
                tasks=tasks,
                execution=execution_message.to_dict(),
                validation=validation_message.to_dict(),
                emitted_messages=[message.to_dict() for message in emitted],
            )

        repair_messages = self.registry.dispatch(runtime, validation_message)
        emitted.extend(repair_messages)
        repair_message = self._latest_of_type(repair_messages, ("RepairSuggested",))

        return ExecutionLoopResult(
            request=request,
            ok=False,
            tasks=tasks,
            execution=execution_message.to_dict(),
            validation=validation_message.to_dict(),
            repair=repair_message.to_dict() if repair_message else None,
            emitted_messages=[message.to_dict() for message in emitted],
        )

    def _tasks_from(self, messages: list[AgentMessage]) -> list[dict[str, Any]]:
        for message in reversed(messages):
            if message.message_type == "TasksPlanned":
                return list(message.payload.get("tasks", []))
        return []

    def _latest_of_type(
        self,
        messages: list[AgentMessage],
        message_types: tuple[str, ...],
    ) -> AgentMessage | None:
        for message in reversed(messages):
            if message.message_type in message_types:
                return message
        return None
