"""Safe deterministic executor agent for Omega-Forge V0.

This agent intentionally supports only a tiny allow-list of actions.
It does not execute arbitrary shell commands.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from omega_forge.agents.base import BaseAgent
from omega_forge.core.context import ContextBuilder, WorkspaceContext
from omega_forge.core.task_queue import TaskQueue
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

        results: list[dict[str, Any]] = []
        executed_count = 0
        blocked_count = 0

        for task in pending[:max_tasks]:
            result = self.execute_task(root=root, title=task.title, context=workspace_context)
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
    def execute_task(root: Path, title: str, context: WorkspaceContext) -> dict[str, Any]:
        normalized = title.lower().strip()

        rules = {
            "write documentation": "documentation",
            "build documentation": "documentation",
            "create documentation": "documentation",
            "write tests": "tests",
            "build tests": "tests",
            "create tests": "tests",
            "build backend": "backend",
            "create backend": "backend",
            "build core": "backend",
            "create core": "backend",
        }

        template_name = rules.get(normalized)
        if template_name:
            path = write_template(root, template_name, context)
            return {
                "executed": True,
                "message": f"Created {template_name} artifact: {path}",
                "path": str(path),
                "template": template_name,
                "project_type": context.project_type,
            }

        return {
            "executed": False,
            "message": f"No safe executor rule matched task: {title}",
            "path": None,
            "template": None,
            "project_type": context.project_type,
        }
