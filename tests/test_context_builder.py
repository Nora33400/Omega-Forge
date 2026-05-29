from omega_forge.core.context import ContextBuilder
from omega_forge.core.task_queue import TaskQueue


def test_context_builder_detects_python_package_layout(tmp_path):
    (tmp_path / "omega_forge" / "core").mkdir(parents=True)
    (tmp_path / "omega_forge" / "agents").mkdir(parents=True)
    (tmp_path / "omega_forge" / "core" / "workspace.py").write_text("", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "README.md").write_text("# Docs\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_sample.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")

    context = ContextBuilder(tmp_path).build()

    assert context.project_type == "python_package"
    assert context.has_docs is True
    assert context.has_tests is True
    assert context.has_core is True
    assert context.has_agents is True
    assert "omega_forge/core/workspace.py" in context.python_files
    assert "tests/test_sample.py" in context.python_files
    assert "docs/README.md" in context.markdown_files


def test_context_builder_detects_generic_workspace(tmp_path):
    (tmp_path / "README.md").write_text("# Generic\n", encoding="utf-8")

    context = ContextBuilder(tmp_path).build()

    assert context.project_type == "generic_workspace"
    assert context.has_docs is False
    assert context.has_tests is False
    assert context.has_core is False
    assert context.has_agents is False
    assert context.python_files == []
    assert context.markdown_files == ["README.md"]


def test_context_builder_reads_task_statuses(tmp_path):
    queue_path = tmp_path / "tasks.json"
    queue = TaskQueue(queue_path)
    pending = queue.add("Build backend")
    done = queue.add("Write tests")
    blocked = queue.add("Invent impossible subsystem")
    queue.set_status(done.id, "done")
    queue.set_status(blocked.id, "blocked")

    context = ContextBuilder(tmp_path, queue_path=queue_path).build()

    assert context.pending_tasks == [pending.title]
    assert context.done_tasks == [done.title]
    assert context.blocked_tasks == [blocked.title]


def test_context_builder_ignores_cache_directories(tmp_path):
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "ignored.py").write_text("", encoding="utf-8")
    (tmp_path / ".pytest_cache").mkdir()
    (tmp_path / ".pytest_cache" / "ignored.md").write_text("", encoding="utf-8")
    (tmp_path / "main.py").write_text("", encoding="utf-8")

    context = ContextBuilder(tmp_path).build()

    assert context.project_type == "python_project"
    assert "main.py" in context.python_files
    assert "__pycache__/ignored.py" not in context.python_files
    assert ".pytest_cache/ignored.md" not in context.markdown_files
