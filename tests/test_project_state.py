from omega_forge.core.project_state import ProjectState


def test_project_state_goal_persists(tmp_path):
    path = tmp_path / "state.json"
    state = ProjectState(path)

    state.set_goal("Build the forge")

    reloaded = ProjectState(path)
    assert reloaded.data.goal == "Build the forge"
    assert len(reloaded.data.history) >= 1


def test_project_state_task_counters(tmp_path):
    path = tmp_path / "state.json"
    state = ProjectState(path)

    state.record_completed_task()
    state.record_failed_task()

    reloaded = ProjectState(path)
    assert reloaded.data.completed_tasks == 1
    assert reloaded.data.failed_tasks == 1


def test_project_state_report_tracking(tmp_path):
    path = tmp_path / "state.json"
    state = ProjectState(path)

    state.add_report("reports/latest_report.md")

    reloaded = ProjectState(path)
    assert reloaded.data.reports == ["reports/latest_report.md"]
    assert reloaded.summary()["reports"] == 1
