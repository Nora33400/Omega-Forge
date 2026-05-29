from omega_forge.agents.reviewer import ReviewerAgent
from omega_forge.core.task_queue import TaskQueue


def test_reviewer_reports_empty_queue(tmp_path):
    queue_path = tmp_path / "tasks.json"
    TaskQueue(queue_path).save()

    result = ReviewerAgent().run({"queue_path": str(queue_path)})

    assert result.success is True
    assert result.data["severity"] == "attention"
    assert "No tasks found" in result.data["findings"][0]


def test_reviewer_detects_duplicate_titles(tmp_path):
    queue_path = tmp_path / "tasks.json"
    queue = TaskQueue(queue_path)
    queue.add("Build core", description="First")
    queue.add("Build core", description="Second")

    result = ReviewerAgent().run({"queue_path": str(queue_path)})

    assert result.success is True
    assert any("Duplicate task title" in finding for finding in result.data["findings"])


def test_reviewer_accepts_reasonable_task(tmp_path):
    queue_path = tmp_path / "tasks.json"
    queue = TaskQueue(queue_path)
    queue.add("Build core", description="Create stable foundation", priority=3)

    result = ReviewerAgent().run({"queue_path": str(queue_path)})

    assert result.success is True
    assert result.data["severity"] == "ok"
    assert result.data["findings"] == []
