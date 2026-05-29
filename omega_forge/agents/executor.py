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
        queue = TaskQueue(queue_path)
        pending = queue.pending()

        if not pending:
            return self.ok("No pending task to execute", {"executed": False})

        task = sorted(pending, key=lambda item: item.priority)[0]
        result = self.execute_task(root=root, title=task.title)

        if result["executed"]:
            queue.set_status(task.id, "done", note=result["message"])
            return self.ok(result["message"], {"executed": True, "task_id": task.id, **result})

        queue.set_status(task.id, "blocked", note=result["message"])
        return self.fail(result["message"], {"executed": False, "task_id": task.id, **result})

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
