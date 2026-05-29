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

    def __init__(self, queue: TaskQueue, state: ProjectState) -> None:
        self.queue = queue
        self.state = state

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
        lines.append(self._recommendation(task_summary))
        lines.append("")
        return "\n".join(lines)

    def write(self, path: str | Path = "reports/latest_report.md") -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(self.build_markdown(), encoding="utf-8")
        self.state.add_report(output)
        return output

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
    def _recommendation(summary: dict[str, int]) -> str:
        if summary.get("failed", 0) > 0:
            return "Repair failed tasks before adding new scope."
        if summary.get("blocked", 0) > 0:
            return "Resolve blocked tasks or split them into smaller tasks."
        if summary.get("pending", 0) > 0:
            return "Pick the highest-priority pending task and execute it."
        return "No pending task. Generate a new plan from the current specification."
