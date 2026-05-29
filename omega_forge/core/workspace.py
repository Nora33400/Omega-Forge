"""Workspace orchestration for Omega-Forge V0."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from omega_forge.agents.executor import ExecutorAgent
from omega_forge.agents.planner import PlannerAgent
from omega_forge.agents.reviewer import ReviewerAgent
from omega_forge.agents.tester import TesterAgent
from omega_forge.core.project_state import ProjectState
from omega_forge.core.report import ReportGenerator
from omega_forge.core.task_queue import TaskQueue


@dataclass
class WorkspaceRunResult:
    spec_path: str
    planner: dict[str, Any]
    executor: dict[str, Any]
    reviewer: dict[str, Any]
    tester: dict[str, Any]
    report_path: str


class ForgeWorkspace:
    """Coordinate the minimal Omega-Forge V0 loop."""

    def __init__(self, root: str | Path = ".", max_tasks_per_run: int = 3) -> None:
        self.root = Path(root)
        self.max_tasks_per_run = max_tasks_per_run
        self.queue_path = self.root / "omega_forge_tasks.json"
        self.state_path = self.root / "omega_forge_state.json"
        self.report_path = self.root / "reports" / "latest_report.md"

    def queue(self) -> TaskQueue:
        return TaskQueue(self.queue_path)

    def state(self) -> ProjectState:
        return ProjectState(self.state_path)

    def initialize(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.queue().save()
        state = self.state()
        state.add_event("ForgeWorkspace initialized")

    def run_spec(self, spec_path: str | Path) -> WorkspaceRunResult:
        spec = Path(spec_path)
        if not spec.is_absolute():
            spec = self.root / spec

        planner_result = PlannerAgent().run(
            {"spec_path": str(spec), "queue_path": str(self.queue_path)}
        )
        executor_result = ExecutorAgent().run(
            {
                "root": str(self.root),
                "queue_path": str(self.queue_path),
                "max_tasks": self.max_tasks_per_run,
            }
        )
        reviewer_result = ReviewerAgent().run({"queue_path": str(self.queue_path)})
        tester_result = TesterAgent().run({"root": str(self.root)})

        agent_results = {
            "planner": planner_result.__dict__,
            "executor": executor_result.__dict__,
            "reviewer": reviewer_result.__dict__,
            "tester": tester_result.__dict__,
        }
        report = ReportGenerator(
            queue=self.queue(),
            state=self.state(),
            agent_results=agent_results,
        )
        written = report.write(self.report_path)

        return WorkspaceRunResult(
            spec_path=str(spec),
            planner=planner_result.__dict__,
            executor=executor_result.__dict__,
            reviewer=reviewer_result.__dict__,
            tester=tester_result.__dict__,
            report_path=str(written),
        )
