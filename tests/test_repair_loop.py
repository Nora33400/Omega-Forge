import sys

from omega_forge.core.forge_runtime import ForgeRuntime
from omega_forge.core.repair_loop import RepairLoop


def make_workspace(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "app.py").write_text("print('hello')\n", encoding="utf-8")
    return workspace


def test_repair_loop_validation_success(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path), sandbox_root=tmp_path / "sandboxes")
    loop = RepairLoop()

    result = loop.run_validation_command(
        runtime,
        [sys.executable, "-c", "print('ok')"],
    )

    assert result.ok is True
    assert result.validation_message is not None
    assert result.validation_message.message_type == "ValidationPassed"
    assert result.repair_message is None


def test_repair_loop_validation_failure_generates_patch_plan(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path), sandbox_root=tmp_path / "sandboxes")
    loop = RepairLoop()

    result = loop.run_validation_command(
        runtime,
        [sys.executable, "-c", "import sys; sys.exit(3)"],
    )

    assert result.ok is False
    assert result.validation_message is not None
    assert result.validation_message.message_type == "ValidationFailed"
    assert result.repair_message is not None
    assert result.repair_message.message_type == "RepairSuggested"
    assert result.patch_plan is not None


def test_repair_loop_records_failure_memory(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path), sandbox_root=tmp_path / "sandboxes")
    loop = RepairLoop()

    loop.run_validation_command(
        runtime,
        [sys.executable, "-c", "import sys; sys.exit(4)"],
    )

    assert runtime.failure_memory.summary()["total"] == 1


def test_repair_loop_process_execution_directly(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path), sandbox_root=tmp_path / "sandboxes")
    loop = RepairLoop()

    _session, execution, _report = runtime.run_in_sandbox(
        [sys.executable, "-c", "print('hello')"]
    )

    result = loop.process_execution(runtime, execution)

    assert result.ok is True
    assert result.execution is not None
    assert result.validation_message.message_type == "ValidationPassed"
