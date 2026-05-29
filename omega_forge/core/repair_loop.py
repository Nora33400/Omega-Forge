"""Conservative repair loop for Omega-Forge.

RepairLoop V1 does not mutate source code automatically. It connects validation
failure handling, patch planning, sandbox validation, and event dispatch into a
single auditable loop.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from omega_forge.core.agent_message import AgentMessage
from omega_forge.core.agents import AgentRegistry, RepairAgent, ValidatorAgent
from omega_forge.core.forge_runtime import ForgeRuntime
from omega_forge.core.patch_plan import PatchPlan
from omega_forge.core.sandbox_manager import ExecutionResult


@dataclass
class RepairLoopResult:
    """Result of one conservative repair loop run."""

    ok: bool
    validation_message: AgentMessage | None = None
    repair_message: AgentMessage | None = None
    patch_plan: dict[str, Any] | None = None
    execution: dict[str, Any] | None = None
    emitted_messages: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.validation_message is not None:
            payload["validation_message"] = self.validation_message.to_dict()
        if self.repair_message is not None:
            payload["repair_message"] = self.repair_message.to_dict()
        return payload


class RepairLoop:
    """Run validation and conservative repair planning."""

    def __init__(self) -> None:
        self.registry = AgentRegistry()
        self.registry.register(ValidatorAgent())
        self.registry.register(RepairAgent())

    def run_validation_command(
        self,
        runtime: ForgeRuntime,
        command: list[str],
        timeout_seconds: int = 30,
    ) -> RepairLoopResult:
        _session, execution, _report = runtime.run_in_sandbox(
            command,
            timeout_seconds=timeout_seconds,
        )
        return self.process_execution(runtime, execution)

    def process_execution(
        self,
        runtime: ForgeRuntime,
        execution: ExecutionResult,
    ) -> RepairLoopResult:
        execution_message = runtime.emit(
            "repair_loop",
            "ExecutionCompleted",
            payload=execution.to_dict(),
        )
        emitted = self.registry.dispatch(runtime, execution_message)

        validation_message = self._latest_of_type(emitted, ("ValidationPassed", "ValidationFailed"))
        if validation_message is None:
            return RepairLoopResult(
                ok=False,
                execution=execution.to_dict(),
                emitted_messages=[message.to_dict() for message in emitted],
            )

        if validation_message.message_type == "ValidationPassed":
            return RepairLoopResult(
                ok=True,
                validation_message=validation_message,
                execution=execution.to_dict(),
                emitted_messages=[message.to_dict() for message in emitted],
            )

        repair_emitted = self.registry.dispatch(runtime, validation_message)
        repair_message = self._latest_of_type(repair_emitted, ("RepairSuggested",))
        patch_plan = None
        if repair_message is not None:
            patch_plan = repair_message.payload.get("patch_plan")

        return RepairLoopResult(
            ok=False,
            validation_message=validation_message,
            repair_message=repair_message,
            patch_plan=patch_plan,
            execution=execution.to_dict(),
            emitted_messages=[message.to_dict() for message in emitted + repair_emitted],
        )

    def approve_plan(self, plan: PatchPlan) -> PatchPlan:
        """Mark a patch plan approved without applying it."""

        plan.mark("approved")
        return plan

    def _latest_of_type(
        self,
        messages: list[AgentMessage],
        message_types: tuple[str, ...],
    ) -> AgentMessage | None:
        for message in reversed(messages):
            if message.message_type in message_types:
                return message
        return None
