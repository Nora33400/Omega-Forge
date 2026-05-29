from omega_forge.agents.executor import ExecutorAgent
from omega_forge.core.task_queue import TaskQueue


def test_executor_creates_backend_artifact(tmp_path):
    queue_path = tmp_path / "tasks.json"
    queue = TaskQueue(queue_path)
    queue.add("Build backend")

    result = ExecutorAgent().run({"root": str(tmp_path), "queue_path": str(queue_path)})

    assert result.success is True
    assert result.data["executed"] is True
    assert (tmp_path / "omega_forge" / "generated_backend.py").exists()

    reloaded = TaskQueue(queue_path)
    assert reloaded.tasks[0].status == "done"


def test_executor_creates_test_artifact(tmp_path):
    queue_path = tmp_path / "tasks.json"
    queue = TaskQueue(queue_path)
    queue.add("Write tests")

    result = ExecutorAgent().run({"root": str(tmp_path), "queue_path": str(queue_path)})

    assert result.success is True
    assert result.data["executed"] is True
    assert (tmp_path / "tests" / "test_generated_placeholder.py").exists()


def test_executor_creates_documentation_artifact(tmp_path):
    queue_path = tmp_path / "tasks.json"
    queue = TaskQueue(queue_path)
    queue.add("Write documentation")

    result = ExecutorAgent().run({"root": str(tmp_path), "queue_path": str(queue_path)})

    assert result.success is True
    assert result.data["executed"] is True
    assert (tmp_path / "docs" / "generated.md").exists()


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
