"""Safe deterministic executor agent for Omega-Forge V0.

This agent intentionally supports only a tiny allow-list of actions.
It does not execute arbitrary shell commands.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from omega_forge.agents.base import BaseAgent
from omega_forge.core.task_queue import TaskQueue


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

        results: list[dict[str, Any]] = []
        executed_count = 0
        blocked_count = 0

        for task in pending[:max_tasks]:
            result = self.execute_task(root=root, title=task.title)
            result = {"task_id": task.id, "task_title": task.title, **result}
            results.append(result)

            if result["executed"]:
                executed_count += 1
                queue.set_status(task.id, "done", note=result["message"])
            else:
                blocked_count += 1
                queue.set_status(task.id, "blocked", note=result["message"])

        message = f"Executed {executed_count} task(s), blocked {blocked_count} task(s)"
        success = executed_count > 0 and blocked_count == 0
        data = {
            "executed": executed_count > 0,
            "executed_count": executed_count,
            "blocked_count": blocked_count,
            "max_tasks": max_tasks,
            "results": results,
        }
        if success:
            return self.ok(message, data)
        return self.fail(message, data)

    @staticmethod
    def execute_task(root: Path, title: str) -> dict[str, Any]:
        normalized = title.lower().strip()

        if normalized in {"write documentation", "build documentation", "create documentation"}:
            path = root / "docs" / "generated.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text("# Generated Documentation\n\nCreated by Omega-Forge ExecutorAgent.\n", encoding="utf-8")
            return {"executed": True, "message": f"Created documentation file: {path}", "path": str(path)}

        if normalized in {"write tests", "build tests", "create tests"}:
            path = root / "tests" / "test_generated_placeholder.py"
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text(
                    "def test_generated_placeholder():\n    assert True\n",
                    encoding="utf-8",
                )
            return {"executed": True, "message": f"Created placeholder test file: {path}", "path": str(path)}

        if normalized in {"build backend", "create backend"}:
            path = root / "omega_forge" / "generated_backend.py"
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text(
                    "\"\"\"Generated backend placeholder.\"\"\"\n\n"
                    "def healthcheck():\n    return {\"status\": \"ok\"}\n",
                    encoding="utf-8",
                )
            return {"executed": True, "message": f"Created backend placeholder: {path}", "path": str(path)}

        return {
            "executed": False,
            "message": f"No safe executor rule matched task: {title}",
            "path": None,
        }
