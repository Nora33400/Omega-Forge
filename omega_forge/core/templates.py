"""Artifact templates for Omega-Forge.

Templates keep the executor small while making generated files easier to improve.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class ArtifactTemplate:
    name: str
    output_path: str
    render: Callable[[], str]


def backend_template() -> str:
    return '''"""Generated backend module for Omega-Forge.

This module is intentionally minimal. It proves that the executor can turn
an allowed task into a Python artifact that can be imported and tested.
"""

from __future__ import annotations


def healthcheck() -> dict[str, str]:
    """Return a minimal service health payload."""

    return {"status": "ok", "service": "omega_forge_generated_backend"}
'''


def test_template() -> str:
    return '''from omega_forge.generated_backend import healthcheck


def test_generated_backend_healthcheck():
    assert healthcheck()["status"] == "ok"
'''


def documentation_template() -> str:
    return '''# Generated Documentation

This document was created by Omega-Forge ExecutorAgent.

## Purpose

Provide a first generated documentation artifact from a planned task.

## Current limitations

- Template-based output only.
- No LLM synthesis yet.
- No project-specific deep analysis yet.

## Next improvement

Replace static sections with context-aware generation from the project state,
task queue, and repository files.
'''


TEMPLATES: dict[str, ArtifactTemplate] = {
    "backend": ArtifactTemplate(
        name="backend",
        output_path="omega_forge/generated_backend.py",
        render=backend_template,
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


def write_template(root: Path, template_name: str) -> Path:
    template = TEMPLATES[template_name]
    output = root / template.output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template.render(), encoding="utf-8")
    return output
