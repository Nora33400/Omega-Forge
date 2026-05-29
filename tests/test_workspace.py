from omega_forge.core.task_queue import TaskQueue
from omega_forge.core.workspace import ForgeWorkspace


def test_workspace_runs_full_v0_loop(tmp_path):
    spec = tmp_path / "SPEC.md"
    spec.write_text("- Build core\n- Write tests\n", encoding="utf-8")

    workspace = ForgeWorkspace(tmp_path)
    workspace.initialize()
    result = workspace.run_spec("SPEC.md")

    assert result.spec_path == str(spec)
    assert result.planner["success"] is True
    assert result.reviewer["success"] is True
    assert result.tester["success"] is True

    queue = TaskQueue(tmp_path / "omega_forge_tasks.json")
    assert [task.title for task in queue.tasks] == ["Build core", "Write tests"]

    report_path = tmp_path / "reports" / "latest_report.md"
    assert (tmp_path / "omega_forge_state.json").exists()
    assert report_path.exists()

    report = report_path.read_text(encoding="utf-8")
    assert "## Agent run summary" in report
    assert "planner: ok" in report
    assert "created tasks: 2" in report
    assert "reviewer: ok" in report
    assert "findings: 0" in report
    assert "tester: ok" in report
    assert "score:" in report
    assert "Execute next task:" in report
    assert "Build core" in report


def test_workspace_initialize_creates_state_files(tmp_path):
    workspace = ForgeWorkspace(tmp_path)
    workspace.initialize()

    assert (tmp_path / "omega_forge_tasks.json").exists()
    assert (tmp_path / "omega_forge_state.json").exists()
