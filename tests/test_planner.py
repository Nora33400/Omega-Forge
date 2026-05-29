from omega_forge.agents.planner import PlannerAgent
from omega_forge.core.task_queue import TaskQueue


def test_extract_task_titles_from_markdown():
    markdown = """
# Plan

- Create backend
- [ ] Add tests
* Write documentation
+ Prepare release
"""

    titles = PlannerAgent.extract_task_titles(markdown)

    assert titles == [
        "Create backend",
        "Add tests",
        "Write documentation",
        "Prepare release",
    ]


def test_planner_creates_tasks_from_spec(tmp_path):
    spec = tmp_path / "SPEC.md"
    queue_path = tmp_path / "tasks.json"
    spec.write_text("- Build core\n- Write tests\n", encoding="utf-8")

    agent = PlannerAgent()
    result = agent.run({"spec_path": str(spec), "queue_path": str(queue_path)})

    assert result.success is True
    assert len(result.data["created_task_ids"]) == 2

    queue = TaskQueue(queue_path)
    assert [task.title for task in queue.tasks] == ["Build core", "Write tests"]


def test_planner_fails_when_spec_missing(tmp_path):
    missing = tmp_path / "missing.md"
    agent = PlannerAgent()

    result = agent.run({"spec_path": str(missing)})

    assert result.success is False
    assert "not found" in result.message
