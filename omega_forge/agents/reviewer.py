"""Reviewer agent for Omega-Forge V0."""

from __future__ import annotations

from collections import Counter
from typing import Any

from omega_forge.agents.base import AgentResult, BaseAgent
from omega_forge.core.task_queue import TaskQueue


class ReviewerAgent(BaseAgent):
    """Review task quality and produce simple recommendations."""

    name = "reviewer"
    role = "task_quality_review"

    def run(self, context: dict[str, Any]) -> AgentResult:
        queue_path = context.get("queue_path", "omega_forge_tasks.json")
        queue = TaskQueue(queue_path)
        findings = self.review_queue(queue)
        severity = "ok" if not findings else "attention"
        return self.ok(
            message=f"Review complete: {len(findings)} findings",
            data={"severity": severity, "findings": findings},
        )

    @staticmethod
    def review_queue(queue: TaskQueue) -> list[str]:
        findings: list[str] = []
        tasks = queue.list()

        if not tasks:
            findings.append("No tasks found. Generate a plan from a specification.")
            return findings

        titles = [task.title.strip().lower() for task in tasks]
        duplicates = [title for title, count in Counter(titles).items() if count > 1]
        for title in duplicates:
            findings.append(f"Duplicate task title detected: {title}")

        for task in tasks:
            if len(task.title.strip()) < 4:
                findings.append(f"Task title too short: {task.id}")
            if len(task.description.strip()) == 0:
                findings.append(f"Task has no description: {task.title}")
            if task.priority < 1 or task.priority > 5:
                findings.append(f"Task priority outside 1..5: {task.title}")

        pending = queue.list("pending")
        if len(pending) > 20:
            findings.append("Too many pending tasks. Split work into a smaller sprint.")

        return findings
