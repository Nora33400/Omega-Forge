"""Minimal repair agent for Omega-Forge.

The repair agent does not modify code directly yet. It converts validation
failures into explicit repair instructions that can be queued, reviewed, or
handled by a future auto-repair loop.
"""

from __future__ import annotations

from typing import Any

from omega_forge.agents.base import BaseAgent


class RepairAgent(BaseAgent):
    """Convert failed artifact validation into a repair plan."""

    name = "repair"
    role = "repair_planning"

    def run(self, context: dict[str, Any]):
        validation = context.get("validation") or {}
        task_title = context.get("task_title", "unknown task")
        artifact_path = validation.get("path") or context.get("path")
        errors = validation.get("errors") or []

        if not errors:
            return self.ok(
                "No repair needed",
                {
                    "repair_needed": False,
                    "task_title": task_title,
                    "artifact_path": artifact_path,
                    "repair_task": None,
                    "errors": [],
                },
            )

        repair_task = self._build_repair_task(task_title, artifact_path, errors)
        return self.fail(
            "Repair required",
            {
                "repair_needed": True,
                "task_title": task_title,
                "artifact_path": artifact_path,
                "repair_task": repair_task,
                "errors": errors,
            },
        )

    @staticmethod
    def _build_repair_task(task_title: str, artifact_path: str | None, errors: list[str]) -> str:
        target = artifact_path or "unknown artifact"
        first_error = errors[0] if errors else "unknown validation error"
        return (
            f"Repair artifact generated for task '{task_title}': "
            f"{target}. Validation error: {first_error}"
        )
