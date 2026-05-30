import sys

from omega_forge.core.execution_loop import ExecutionLoop
from omega_forge.core.forge_runtime import ForgeRuntime


def make_workspace(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "app.py").write_text("print('hello')\n", encoding="utf-8")
    return workspace


def test_execution_loop_success_path(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path), sandbox_root=tmp_path / "sandboxes")
    loop = ExecutionLoop()

    result = loop.run(
        runtime,
        request="check python",
        command=[sys.executable, "-c", "print('ok')"],
    )

    assert result.ok is True
    assert result.tasks
    assert result.execution is not None
    assert result.validation is not None
    assert result.validation["message_type"] == "ValidationPassed"
    assert result.repair is None


def test_execution_loop_failure_path_suggests_repair(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path), sandbox_root=tmp_path / "sandboxes")
    loop = ExecutionLoop()

    result = loop.run(
        runtime,
        request="run failing command",
        command=[sys.executable, "-c", "import sys; sys.exit(9)"],
    )

    assert result.ok is False
    assert result.execution is not None
    assert result.validation is not None
    assert result.validation["message_type"] == "ValidationFailed"
    assert result.repair is not None
    assert result.repair["message_type"] == "RepairSuggested"
    assert runtime.failure_memory.summary()["total"] == 1


def test_execution_loop_rejects_invalid_command(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path), sandbox_root=tmp_path / "sandboxes")
    loop = ExecutionLoop()

    result = loop.run(
        runtime,
        request="bad command",
        command=[],
    )

    assert result.ok is False
    assert result.execution is not None
    assert result.execution["message_type"] == "ExecutionRejected"
    assert result.validation is None
    assert result.repair is None


def test_execution_loop_tracks_emitted_messages(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path), sandbox_root=tmp_path / "sandboxes")
    loop = ExecutionLoop()

    result = loop.run(
        runtime,
        request="check messages",
        command=[sys.executable, "-c", "print('ok')"],
    )

    message_types = [message["message_type"] for message in result.emitted_messages]

    assert "UserRequest" in message_types
    assert "TasksPlanned" in message_types
    assert "ExecuteCommand" in message_types
    assert "ExecutionCompleted" in message_types
    assert "ValidationPassed" in message_types
