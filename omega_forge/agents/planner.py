"""Deterministic planner agent for Omega-Forge V0."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from omega_forge.agents.base import AgentResult, BaseAgent
from omega_forge.core.task_queue import TaskQueue


class PlannerAgent(BaseAgent):
    """Convert a Markdown specification into simple tasks.

    V0 intentionally avoids LLM dependency. It extracts actionable lines from
    Markdown bullet lists and checklist items.
    """

    name = "planner"
    role = "spec_to_tasks"

    def run(self, context: dict[str, Any]) -> AgentResult:
        spec_path = context.get("spec_path")
        queue_path = context.get("queue_path", "omega_forge_tasks.json")

        if not spec_path:
            return self.fail("Missing spec_path in context")

        path = Path(spec_path)
        if not path.exists():
            return self.fail(f"Specification not found: {path}")

        text = path.read_text(encoding="utf-8")
        task_titles = self.extract_task_titles(text)

        queue = TaskQueue(queue_path)
        created = []
        for title in task_titles:
            task = queue.add(title=title, description=f"Generated from {path}", priority=3)
            created.append(task.id)

        return self.ok(
            message=f"Created {len(created)} tasks from {path}",
            data={"created_task_ids": created, "source": str(path)},
        )

    @staticmethod
    def extract_task_titles(markdown: str) -> list[str]:
        titles: list[str] = []
        for raw_line in markdown.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            candidate = PlannerAgent._extract_from_line(line)
            if candidate and candidate not in titles:
                titles.append(candidate)
        return titles

    @staticmethod
    def _extract_from_line(line: str) -> str | None:
        markers = ["- [ ]", "- [x]", "-", "*", "+"]
        for marker in markers:
            if line.startswith(marker):
                candidate = line[len(marker):].strip()
                return PlannerAgent._clean_candidate(candidate)
        return None

    @staticmethod
    def _clean_candidate(candidate: str) -> str | None:
        candidate = candidate.strip()
        if not candidate:
            return None
        lowered = candidate.lower()
        ignored = {"x", "done", "todo", "task", "tasks"}
        if lowered in ignored:
            return None
        return candidate
