from omega_forge.core.context import WorkspaceContext
from omega_forge.core.template_selector import TemplateSelector


def make_context(project_type="python_package", has_docs=True, has_tests=True):
    return WorkspaceContext(
        root=".",
        project_type=project_type,
        has_docs=has_docs,
        has_tests=has_tests,
        has_core=True,
        has_agents=True,
        python_files=["omega_forge/core/workspace.py"],
        markdown_files=["README.md"],
        pending_tasks=[],
        done_tasks=[],
        blocked_tasks=[],
    )


def test_selector_routes_backend_task_for_python_package():
    selection = TemplateSelector().select("Build core", make_context("python_package"))

    assert selection.template_name == "backend"
    assert "python package" in selection.reason


def test_selector_routes_backend_task_for_generic_workspace():
    selection = TemplateSelector().select("Build backend", make_context("generic_workspace"))

    assert selection.template_name == "backend"
    assert "generic workspace" in selection.reason


def test_selector_routes_test_task():
    selection = TemplateSelector().select("Write tests", make_context(has_tests=True))

    assert selection.template_name == "tests"
    assert "test task matched" in selection.reason
    assert "existing tests directory detected" in selection.reason


def test_selector_routes_documentation_task():
    selection = TemplateSelector().select("Write documentation", make_context(has_docs=True))

    assert selection.template_name == "documentation"
    assert "documentation task matched" in selection.reason
    assert "existing docs directory detected" in selection.reason


def test_selector_rejects_unknown_task():
    selection = TemplateSelector().select("Invent impossible subsystem", make_context())

    assert selection.template_name is None
    assert "no template rule matched" in selection.reason
