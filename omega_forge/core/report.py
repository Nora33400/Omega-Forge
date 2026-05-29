"""Markdown report generation for Omega-Forge."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from omega_forge.core.project_state import ProjectState
from omega_forge.core.task_queue import TaskQueue


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReportGenerator:
    """Generate human-readable Markdown reports from project state and tasks."""

    def __init__(
        self,
        queue: TaskQueue,
        state: ProjectState,
        agent_results: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self.queue = queue
        self.state = state
        self.agent_results = agent_results or {}

    def build_markdown(self) -> str:
        state_summary = self.state.summary()
        task_summary = self.queue.summary()
        pending_tasks = self.queue.list("pending")
        failed_tasks = self.queue.list("failed")
        blocked_tasks = self.queue.list("blocked")
        done_tasks = self.queue.list("done")

        lines: list[str] = []
        lines.append("# Omega-Forge Report")
        lines.append("")
        lines.append(f"Generated at: `{utc_now()}`")
        lines.append("")
        lines.append("## Project")
        lines.append("")
        lines.append(f"- Version: `{state_summary['version']}`")
        lines.append(f"- Goal: {state_summary['goal']}")
        lines.append(f"- Completed tasks recorded: {state_summary['completed_tasks']}")
        lines.append(f"- Failed tasks recorded: {state_summary['failed_tasks']}")
        lines.append(f"- Reports known: {state_summary['reports']}")
        lines.append("")
        lines.append("## Agent run summary")
        lines.append("")
        lines.extend(self._agent_result_lines())
        lines.append("")
        lines.append("## Task summary")
        lines.append("")
        for key in ["total", "pending", "running", "done", "failed", "blocked"]:
            lines.append(f"- {key}: {task_summary.get(key, 0)}")
        lines.append("")
        lines.append("## Pending tasks")
        lines.append("")
        lines.extend(self._task_lines(pending_tasks, empty="No pending tasks."))
        lines.append("")
        lines.append("## Failed tasks")
        lines.append("")
        lines.extend(self._task_lines(failed_tasks, empty="No failed tasks."))
        lines.append("")
        lines.append("## Blocked tasks")
        lines.append("")
        lines.extend(self._task_lines(blocked_tasks, empty="No blocked tasks."))
        lines.append("")
        lines.append("## Recently completed")
        lines.append("")
        lines.extend(self._task_lines(done_tasks[-10:], empty="No completed tasks yet."))
        lines.append("")
        lines.append("## Recommended next action")
        lines.append("")
        lines.append(self._recommendation(task_summary, pending_tasks))
        lines.append("")
        return "\n".join(lines)

    def write(self, path: str | Path = "reports/latest_report.md") -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(self.build_markdown(), encoding="utf-8")
        self.state.add_report(output)
        return output

    def _agent_result_lines(self) -> list[str]:
        if not self.agent_results:
            return ["No agent run metadata was attached to this report."]

        lines: list[str] = []
        for name in ["planner", "executor", "reviewer", "tester"]:
            result = self.agent_results.get(name)
            if not result:
                lines.append(f"- {name}: not run")
                continue

            success = result.get("success")
            status = "ok" if success else "failed"
            lines.append(f"- {name}: {status} — {result.get('message', 'No message')}")

            data = result.get("data") or {}
            if name == "planner" and data.get("created_task_ids") is not None:
                lines.append(f"  - created tasks: {len(data.get('created_task_ids', []))}")
            if name == "executor":
                lines.append(f"  - executed: {data.get('executed', False)}")
                if data.get("task_id"):
                    lines.append(f"  - task id: {data.get('task_id')}")
                if data.get("path"):
                    lines.append(f"  - artifact: {data.get('path')}")
            if name == "reviewer":
                findings = data.get("findings", [])
                lines.append(f"  - findings: {len(findings)}")
                for finding in findings[:10]:
                    lines.append(f"    - {finding}")
            if name == "tester" and data.get("score") is not None:
                lines.append(f"  - score: {data.get('score')}/{data.get('max_score')}")

        return lines

    @staticmethod
    def _task_lines(tasks: list[Any], empty: str) -> list[str]:
        if not tasks:
            return [empty]
        lines = []
        for task in tasks:
            lines.append(f"- `{task.id}` [{task.status}] P{task.priority} — {task.title}")
            if task.description:
                lines.append(f"  - {task.description}")
        return lines

    @staticmethod
    def _recommendation(summary: dict[str, int], pending_tasks: list[Any]) -> str:
        if summary.get("failed", 0) > 0:
            return "Repair failed tasks before adding new scope."
        if summary.get("blocked", 0) > 0:
            return "Resolve blocked tasks or split them into smaller tasks."
        if pending_tasks:
            first = sorted(pending_tasks, key=lambda task: task.priority)[0]
            return f"Execute next task: `{first.id}` — {first.title}."
        return "No pending task. Generate a new plan from the current specification."
