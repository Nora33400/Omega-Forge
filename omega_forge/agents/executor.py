"""Safe deterministic executor agent for Omega-Forge V0.

This agent intentionally supports only a tiny allow-list of actions.
It does not execute arbitrary shell commands.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from omega_forge.agents.base import BaseAgent
from omega_forge.core.artifact_validator import ArtifactValidator
from omega_forge.core.context import ContextBuilder, WorkspaceContext
from omega_forge.core.task_queue import TaskQueue
from omega_forge.core.template_selector import TemplateSelector
from omega_forge.core.templates import write_template


class ExecutorAgent(BaseAgent):
    """Execute simple allow-listed task patterns."""

    name = "executor"
    role = "safe_task_execution"

    def run(self, context: dict[str, Any]):
        root = Path(context.get("root", "."))
        queue_path = context.get("queue_path", root / "omega_forge_tasks.json")
        max_tasks = int(context.get("max_tasks", 1))
        max_tasks = max(1, min(max_tasks, 10))

        queue = TaskQueue(queue_path)
        pending = sorted(queue.pending(), key=lambda item: item.priority)

        if not pending:
            return self.ok("No pending task to execute", {"executed": False, "results": []})

        workspace_context = ContextBuilder(root=root, queue_path=queue_path).build()
        selector = TemplateSelector()
        validator = ArtifactValidator()

        results: list[dict[str, Any]] = []
        executed_count = 0
        blocked_count = 0

        for task in pending[:max_tasks]:
            result = self.execute_task(
                root=root,
                title=task.title,
                context=workspace_context,
                selector=selector,
                validator=validator,
            )
            result = {"task_id": task.id, "task_title": task.title, **result}
            results.append(result)

            if result["executed"]:
                executed_count += 1
                queue.set_status(task.id, "done", note=result["message"])
                workspace_context = ContextBuilder(root=root, queue_path=queue_path).build()
            else:
                blocked_count += 1
                queue.set_status(task.id, "blocked", note=result["message"])
                workspace_context = ContextBuilder(root=root, queue_path=queue_path).build()

        message = f"Executed {executed_count} task(s), blocked {blocked_count} task(s)"
        success = executed_count > 0 and blocked_count == 0
        data = {
            "executed": executed_count > 0,
            "executed_count": executed_count,
            "blocked_count": blocked_count,
            "max_tasks": max_tasks,
            "context": workspace_context.to_dict(),
            "results": results,
        }
        if success:
            return self.ok(message, data)
        return self.fail(message, data)

    @staticmethod
    def execute_task(
        root: Path,
        title: str,
        context: WorkspaceContext,
        selector: TemplateSelector | None = None,
        validator: ArtifactValidator | None = None,
    ) -> dict[str, Any]:
        selector = selector or TemplateSelector()
        validator = validator or ArtifactValidator()
        selection = selector.select(title, context)

        if selection.template_name:
            path = write_template(root, selection.template_name, context)
            validation = validator.validate(root, path)
            if not validation.ok:
                return {
                    "executed": False,
                    "message": f"Artifact validation failed for {path}",
                    "path": str(path),
                    "template": selection.template_name,
                    "selection_reason": selection.reason,
                    "project_type": context.project_type,
                    "validation": validation.__dict__,
                }
            return {
                "executed": True,
                "message": f"Created and validated {selection.template_name} artifact: {path}",
                "path": str(path),
                "template": selection.template_name,
                "selection_reason": selection.reason,
                "project_type": context.project_type,
                "validation": validation.__dict__,
            }

        return {
            "executed": False,
            "message": selection.reason,
            "path": None,
            "template": None,
            "selection_reason": selection.reason,
            "project_type": context.project_type,
            "validation": None,
        }
