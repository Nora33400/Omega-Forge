"""Tester agent for Omega-Forge V0."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from omega_forge.agents.base import BaseAgent


class TesterAgent(BaseAgent):
    name = "tester"
    role = "project_validation"

    def run(self, context: dict[str, Any]):
        root = Path(context.get("root", "."))

        checks = {
            "docs": (root / "docs").exists(),
            "core": (root / "omega_forge" / "core").exists(),
            "agents": (root / "omega_forge" / "agents").exists(),
            "tests": (root / "tests").exists(),
        }

        score = sum(1 for value in checks.values() if value)

        return self.ok(
            message=f"Validation score: {score}/{len(checks)}",
            data={
                "score": score,
                "max_score": len(checks),
                "checks": checks,
            },
        )
