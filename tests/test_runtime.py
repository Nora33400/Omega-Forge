import sys

from omega_forge.core.forge_runtime import ForgeRuntime


def make_workspace(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "app.py").write_text("print('hello')\n", encoding="utf-8")
    return workspace


def test_runtime_emits_messages(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path))

    message = runtime.emit("tester", "Ping", payload={"ok": True})

    assert message.sender == "tester"
    assert message.message_type == "Ping"
    assert runtime.bus.history() == [message]


def test_runtime_indexes_workspace_into_knowledge_graph(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path))

    report = runtime.index_workspace()

    assert report.ok is True
    assert report.data["index"]["file_count"] == 1
    assert report.data["knowledge"]["node_types"]["Project"] == 1
    assert report.data["knowledge"]["node_types"]["File"] == 1
    assert any(message["message_type"] == "WorkspaceIndexed" for message in report.messages)


def test_runtime_record_failure_and_plan(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path))

    failure, plan, report = runtime.record_failure_and_plan(
        "ModuleNotFoundError: No module named requests",
        task_title="Build API",
        artifact_path="requirements.txt",
    )

    assert failure.status == "unresolved"
    assert plan.strategy == "add_dependency"
    assert plan.targets[0].path == "requirements.txt"
    assert report.data["knowledge"]["node_types"]["Failure"] == 1
    assert report.data["knowledge"]["node_types"]["PatchPlan"] == 1
    assert any(message["message_type"] == "PatchPlanCreated" for message in report.messages)


def test_runtime_run_in_sandbox_success(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path), sandbox_root=tmp_path / "sandboxes")

    _session, result, report = runtime.run_in_sandbox([sys.executable, "-c", "print('ok')"])

    assert result.ok is True
    assert "ok" in result.stdout
    assert report.ok is True
    assert any(message["message_type"] == "SandboxCommandExecuted" for message in report.messages)


def test_runtime_run_in_sandbox_failure(tmp_path):
    runtime = ForgeRuntime(make_workspace(tmp_path), sandbox_root=tmp_path / "sandboxes")

    _session, result, report = runtime.run_in_sandbox([sys.executable, "-c", "import sys; sys.exit(5)"])

    assert result.ok is False
    assert result.exit_code == 5
    assert report.ok is False
