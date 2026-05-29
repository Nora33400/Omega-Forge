"""Context-aware template selection for Omega-Forge."""

from __future__ import annotations

from dataclasses import dataclass

from omega_forge.core.context import WorkspaceContext


@dataclass(frozen=True)
class TemplateSelection:
    template_name: str | None
    reason: str


class TemplateSelector:
    """Select an artifact template from a task title and workspace context."""

    def select(self, task_title: str, context: WorkspaceContext) -> TemplateSelection:
        normalized = task_title.lower().strip()

        if normalized in {"write documentation", "build documentation", "create documentation"}:
            reason = "documentation task matched"
            if context.has_docs:
                reason += "; existing docs directory detected"
            return TemplateSelection("documentation", reason)

        if normalized in {"write tests", "build tests", "create tests"}:
            reason = "test task matched"
            if context.has_tests:
                reason += "; existing tests directory detected"
            return TemplateSelection("tests", reason)

        if normalized in {"build backend", "create backend", "build core", "create core"}:
            return self._select_backend_template(context)

        return TemplateSelection(None, f"no template rule matched task: {task_title}")

    @staticmethod
    def _select_backend_template(context: WorkspaceContext) -> TemplateSelection:
        python_files = set(context.python_files)
        lower_files = {path.lower() for path in python_files}

        if any("fastapi" in path for path in lower_files) or any(
            path.endswith("api.py") or "/api/" in path for path in lower_files
        ):
            return TemplateSelection(
                "backend_api",
                "backend/core task matched; API-like files detected",
            )

        if "main.py" in lower_files or any(path.endswith("/cli.py") for path in lower_files):
            return TemplateSelection(
                "backend_cli",
                "backend/core task matched; CLI entrypoint detected",
            )

        if context.project_type == "python_package":
            return TemplateSelection(
                "backend_library",
                "backend/core task matched for python package",
            )

        if context.project_type == "python_project":
            return TemplateSelection(
                "backend_cli",
                "backend/core task matched for python project",
            )

        return TemplateSelection(
            "backend_library",
            "backend/core task matched for generic workspace",
        )
