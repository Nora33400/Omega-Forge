"""Generated artifact validation for Omega-Forge."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ArtifactValidationResult:
    ok: bool
    path: str | None
    checks: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class ArtifactValidator:
    """Validate generated artifacts before tasks are marked done."""

    def validate(self, root: str | Path, artifact_path: str | Path | None) -> ArtifactValidationResult:
        if artifact_path is None:
            return ArtifactValidationResult(
                ok=False,
                path=None,
                errors=["No artifact path was provided."],
            )

        root_path = Path(root)
        path = Path(artifact_path)
        if not path.is_absolute():
            path = root_path / path

        checks: list[str] = []
        errors: list[str] = []

        if not path.exists():
            return ArtifactValidationResult(
                ok=False,
                path=str(path),
                checks=checks,
                errors=[f"Artifact does not exist: {path}"],
            )

        checks.append("exists")

        if path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"))
                checks.append("python_syntax")
            except SyntaxError as exc:
                errors.append(f"Python syntax error: {exc}")

        return ArtifactValidationResult(
            ok=not errors,
            path=str(path),
            checks=checks,
            errors=errors,
        )
