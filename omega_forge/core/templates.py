"""Artifact templates for Omega-Forge.

Templates keep the executor small while making generated files easier to improve.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from omega_forge.core.context import WorkspaceContext


@dataclass(frozen=True)
class ArtifactTemplate:
    name: str
    output_path: str
    render: Callable[[WorkspaceContext], str]


def backend_template(context: WorkspaceContext) -> str:
    return backend_library_template(context)


def backend_library_template(context: WorkspaceContext) -> str:
    return f'''"""Generated backend library module for Omega-Forge.

This module was generated from an observed workspace context.
Project type: {context.project_type}
Docs detected: {context.has_docs}
Tests detected: {context.has_tests}
"""

from __future__ import annotations


def healthcheck() -> dict[str, str]:
    """Return a minimal service health payload."""

    return {{
        "status": "ok",
        "service": "omega_forge_generated_backend_library",
        "project_type": "{context.project_type}",
        "mode": "library",
    }}
'''


def backend_cli_template(context: WorkspaceContext) -> str:
    return f'''"""Generated backend CLI module for Omega-Forge."""

from __future__ import annotations

import json


def healthcheck() -> dict[str, str]:
    return {{
        "status": "ok",
        "service": "omega_forge_generated_backend_cli",
        "project_type": "{context.project_type}",
        "mode": "cli",
    }}


def main() -> int:
    print(json.dumps(healthcheck(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def backend_api_template(context: WorkspaceContext) -> str:
    return f'''"""Generated backend API-style module for Omega-Forge.

This is framework-neutral by design: it exposes route-like callables without
requiring FastAPI, Flask, or any other runtime dependency.
"""

from __future__ import annotations


def healthcheck() -> dict[str, str]:
    return {{
        "status": "ok",
        "service": "omega_forge_generated_backend_api",
        "project_type": "{context.project_type}",
        "mode": "api",
    }}


def get_routes() -> dict[str, object]:
    return {{
        "GET /health": healthcheck,
    }}
'''


def test_template(context: WorkspaceContext) -> str:
    return f'''from omega_forge.generated_backend import healthcheck


def test_generated_backend_healthcheck():
    payload = healthcheck()
    assert payload["status"] == "ok"
    assert payload["project_type"] == "{context.project_type}"
    assert payload["mode"] in {{"library", "cli", "api"}}
'''


def documentation_template(context: WorkspaceContext) -> str:
    pending = "\n".join(f"- {title}" for title in context.pending_tasks) or "- No pending tasks"
    done = "\n".join(f"- {title}" for title in context.done_tasks) or "- No completed tasks"
    blocked = "\n".join(f"- {title}" for title in context.blocked_tasks) or "- No blocked tasks"

    return f'''# Generated Documentation

This document was created by Omega-Forge ExecutorAgent from workspace context.

## Context snapshot

- Project type: `{context.project_type}`
- Docs detected: `{context.has_docs}`
- Tests detected: `{context.has_tests}`
- Core detected: `{context.has_core}`
- Agents detected: `{context.has_agents}`
- Python files detected: `{len(context.python_files)}`
- Markdown files detected: `{len(context.markdown_files)}`

## Pending tasks

{pending}

## Completed tasks

{done}

## Blocked tasks

{blocked}

## Next improvement

Use this context snapshot to select richer task-specific generators instead of
static templates.
'''


TEMPLATES: dict[str, ArtifactTemplate] = {
    "backend": ArtifactTemplate(
        name="backend",
        output_path="omega_forge/generated_backend.py",
        render=backend_template,
    ),
    "backend_library": ArtifactTemplate(
        name="backend_library",
        output_path="omega_forge/generated_backend.py",
        render=backend_library_template,
    ),
    "backend_cli": ArtifactTemplate(
        name="backend_cli",
        output_path="omega_forge/generated_backend.py",
        render=backend_cli_template,
    ),
    "backend_api": ArtifactTemplate(
        name="backend_api",
        output_path="omega_forge/generated_backend.py",
        render=backend_api_template,
    ),
    "tests": ArtifactTemplate(
        name="tests",
        output_path="tests/test_generated_backend.py",
        render=test_template,
    ),
    "documentation": ArtifactTemplate(
        name="documentation",
        output_path="docs/generated.md",
        render=documentation_template,
    ),
}


def write_template(root: Path, template_name: str, context: WorkspaceContext) -> Path:
    template = TEMPLATES[template_name]
    output = root / template.output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template.render(context), encoding="utf-8")
    return output
