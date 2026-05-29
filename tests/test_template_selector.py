from omega_forge.core.context import WorkspaceContext
from omega_forge.core.template_selector import TemplateSelector


def make_context(
    project_type="python_package",
    has_docs=True,
    has_tests=True,
    python_files=None,
):
    return WorkspaceContext(
        root=".",
        project_type=project_type,
        has_docs=has_docs,
        has_tests=has_tests,
        has_core=True,
        has_agents=True,
        python_files=python_files or ["omega_forge/core/workspace.py"],
        markdown_files=["README.md"],
        pending_tasks=[],
        done_tasks=[],
        blocked_tasks=[],
    )


def test_selector_routes_backend_task_for_python_package_to_library():
    selection = TemplateSelector().select("Build core", make_context("python_package"))

    assert selection.template_name == "backend_library"
    assert "python package" in selection.reason


def test_selector_routes_backend_task_for_generic_workspace_to_library():
    selection = TemplateSelector().select("Build backend", make_context("generic_workspace"))

    assert selection.template_name == "backend_library"
    assert "generic workspace" in selection.reason


def test_selector_routes_backend_task_with_main_py_to_cli():
    selection = TemplateSelector().select(
        "Build backend",
        make_context(
            project_type="python_project",
            python_files=["main.py", "helpers.py"],
        ),
    )

    assert selection.template_name == "backend_cli"
    assert "CLI entrypoint detected" in selection.reason


def test_selector_routes_backend_task_with_cli_module_to_cli():
    selection = TemplateSelector().select(
        "Build backend",
        make_context(
            project_type="python_package",
            python_files=["omega_forge/cli.py", "omega_forge/core/workspace.py"],
        ),
    )

    assert selection.template_name == "backend_cli"
    assert "CLI entrypoint detected" in selection.reason


def test_selector_routes_backend_task_with_api_py_to_api():
    selection = TemplateSelector().select(
        "Build backend",
        make_context(
            project_type="python_package",
            python_files=["omega_forge/api.py", "omega_forge/core/workspace.py"],
        ),
    )

    assert selection.template_name == "backend_api"
    assert "API-like files detected" in selection.reason


def test_selector_routes_backend_task_with_api_directory_to_api():
    selection = TemplateSelector().select(
        "Build backend",
        make_context(
            project_type="python_package",
            python_files=["omega_forge/api/routes.py", "omega_forge/core/workspace.py"],
        ),
    )

    assert selection.template_name == "backend_api"
    assert "API-like files detected" in selection.reason


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
