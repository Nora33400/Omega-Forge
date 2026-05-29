from omega_forge.agents.executor import ExecutorAgent
from omega_forge.core.task_queue import TaskQueue


def test_executor_creates_backend_artifact(tmp_path):
    queue_path = tmp_path / "tasks.json"
    queue = TaskQueue(queue_path)
    queue.add("Build backend")

    result = ExecutorAgent().run({"root": str(tmp_path), "queue_path": str(queue_path)})

    assert result.success is True
    assert result.data["executed"] is True
    assert result.data["executed_count"] == 1
    assert result.data["blocked_count"] == 0
    backend = tmp_path / "omega_forge" / "generated_backend.py"
    assert backend.exists()
    assert "Project type:" in backend.read_text(encoding="utf-8")

    reloaded = TaskQueue(queue_path)
    assert reloaded.tasks[0].status == "done"


def test_executor_creates_test_artifact(tmp_path):
    queue_path = tmp_path / "tasks.json"
    queue = TaskQueue(queue_path)
    queue.add("Write tests")

    result = ExecutorAgent().run({"root": str(tmp_path), "queue_path": str(queue_path)})

    assert result.success is True
    assert result.data["executed"] is True
    assert (tmp_path / "tests" / "test_generated_backend.py").exists()


def test_executor_creates_documentation_artifact(tmp_path):
    queue_path = tmp_path / "tasks.json"
    queue = TaskQueue(queue_path)
    queue.add("Write documentation")

    result = ExecutorAgent().run({"root": str(tmp_path), "queue_path": str(queue_path)})

    assert result.success is True
    assert result.data["executed"] is True
    docs = tmp_path / "docs" / "generated.md"
    assert docs.exists()
    content = docs.read_text(encoding="utf-8")
    assert "## Context snapshot" in content
    assert "Project type:" in content


def test_executor_runs_multiple_tasks_with_limit(tmp_path):
    queue_path = tmp_path / "tasks.json"
    queue = TaskQueue(queue_path)
    queue.add("Build backend")
    queue.add("Write tests")
    queue.add("Write documentation")

    result = ExecutorAgent().run(
        {"root": str(tmp_path), "queue_path": str(queue_path), "max_tasks": 3}
    )

    assert result.success is True
    assert result.data["executed_count"] == 3
    assert result.data["blocked_count"] == 0
    assert (tmp_path / "omega_forge" / "generated_backend.py").exists()
    assert (tmp_path / "tests" / "test_generated_backend.py").exists()
    assert (tmp_path / "docs" / "generated.md").exists()

    reloaded = TaskQueue(queue_path)
    assert all(task.status == "done" for task in reloaded.tasks)


def test_executor_blocks_unknown_task(tmp_path):
    queue_path = tmp_path / "tasks.json"
    queue = TaskQueue(queue_path)
    queue.add("Invent impossible subsystem")

    result = ExecutorAgent().run({"root": str(tmp_path), "queue_path": str(queue_path)})

    assert result.success is False
    assert result.data["executed"] is False
    assert "No safe executor rule matched" in result.message

    reloaded = TaskQueue(queue_path)
    assert reloaded.tasks[0].status == "blocked"
