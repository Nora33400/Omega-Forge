from omega_forge.core.task_queue import TaskQueue
from omega_forge.core.workspace import ForgeWorkspace


def test_workspace_runs_full_v0_loop(tmp_path):
    spec = tmp_path / "SPEC.md"
    spec.write_text(
        "- Build core\n- Write tests\n- Write documentation\n",
        encoding="utf-8",
    )

    workspace = ForgeWorkspace(tmp_path)
    workspace.initialize()
    result = workspace.run_spec("SPEC.md")

    assert result.spec_path == str(spec)
    assert result.planner["success"] is True
    assert result.executor["success"] is True
    assert result.executor["data"]["executed_count"] == 3
    assert result.executor["data"]["blocked_count"] == 0
    assert result.reviewer["success"] is True
    assert result.tester["success"] is True

    queue = TaskQueue(tmp_path / "omega_forge_tasks.json")
    assert [task.title for task in queue.tasks] == [
        "Build core",
        "Write tests",
        "Write documentation",
    ]
    assert all(task.status == "done" for task in queue.tasks)

    backend = tmp_path / "omega_forge" / "generated_backend.py"
    tests = tmp_path / "tests" / "test_generated_backend.py"
    docs = tmp_path / "docs" / "generated.md"
    report_path = tmp_path / "reports" / "latest_report.md"

    assert backend.exists()
    assert tests.exists()
    assert docs.exists()
    assert (tmp_path / "omega_forge_state.json").exists()
    assert report_path.exists()

    report = report_path.read_text(encoding="utf-8")
    assert "## Agent run summary" in report
    assert "planner: ok" in report
    assert "created tasks: 3" in report
    assert "executor: ok" in report
    assert "executed count: 3" in report
    assert "blocked count: 0" in report
    assert "reviewer: ok" in report
    assert "findings: 0" in report
    assert "tester: ok" in report
    assert "score:" in report
    assert "## Generated artifacts" in report
    assert "generated_backend.py" in report
    assert "test_generated_backend.py" in report
    assert "generated.md" in report
    assert "No pending task" in report


def test_workspace_initialize_creates_state_files(tmp_path):
    workspace = ForgeWorkspace(tmp_path)
    workspace.initialize()

    assert (tmp_path / "omega_forge_tasks.json").exists()
    assert (tmp_path / "omega_forge_state.json").exists()
