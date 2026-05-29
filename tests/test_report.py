from omega_forge.core.project_state import ProjectState
from omega_forge.core.report import ReportGenerator
from omega_forge.core.task_queue import TaskQueue


def test_report_contains_project_and_task_summary(tmp_path):
    queue_path = tmp_path / "tasks.json"
    state_path = tmp_path / "state.json"
    queue = TaskQueue(queue_path)
    state = ProjectState(state_path)

    queue.add("Create report", description="Report must be readable", priority=2)
    state.set_goal("Test reporting")

    report = ReportGenerator(queue=queue, state=state)
    markdown = report.build_markdown()

    assert "# Omega-Forge Report" in markdown
    assert "Test reporting" in markdown
    assert "Create report" in markdown
    assert "pending" in markdown


def test_report_write_creates_file_and_tracks_report(tmp_path):
    queue = TaskQueue(tmp_path / "tasks.json")
    state = ProjectState(tmp_path / "state.json")
    output = tmp_path / "reports" / "latest.md"

    queue.add("Write output")
    report = ReportGenerator(queue=queue, state=state)
    written = report.write(output)

    assert written.exists()
    assert "Omega-Forge Report" in written.read_text(encoding="utf-8")

    reloaded = ProjectState(tmp_path / "state.json")
    assert str(output) in reloaded.data.reports


def test_report_recommends_failed_tasks_first(tmp_path):
    queue = TaskQueue(tmp_path / "tasks.json")
    state = ProjectState(tmp_path / "state.json")
    task = queue.add("Broken task")
    queue.set_status(task.id, "failed")

    report = ReportGenerator(queue=queue, state=state)
    markdown = report.build_markdown()

    assert "Repair failed tasks" in markdown
