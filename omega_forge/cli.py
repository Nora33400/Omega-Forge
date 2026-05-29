"""Minimal command line interface for Omega-Forge."""

from __future__ import annotations

import argparse
from pathlib import Path

from omega_forge.core.report import ReportGenerator
from omega_forge.core.workspace import ForgeWorkspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omega",
        description="Omega-Forge V0 command line interface",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Initialize Omega-Forge state files")

    run = sub.add_parser("run", help="Run the V0 forge loop from a spec file")
    run.add_argument("spec", help="Path to a Markdown specification")

    report = sub.add_parser("report", help="Generate a report from current state")
    report.add_argument("--output", default="reports/latest_report.md")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    workspace = ForgeWorkspace(Path.cwd())

    if args.command == "init":
        workspace.initialize()
        print("Omega-Forge initialized.")
        return 0

    if args.command == "run":
        result = workspace.run_spec(args.spec)
        print("Omega-Forge run complete.")
        print(f"Spec: {result.spec_path}")
        print(f"Report: {result.report_path}")
        print(f"Planner: {result.planner.get('message')}")
        print(f"Reviewer: {result.reviewer.get('message')}")
        print(f"Tester: {result.tester.get('message')}")
        return 0

    if args.command == "report":
        report = ReportGenerator(queue=workspace.queue(), state=workspace.state())
        output = report.write(args.output)
        print(f"Report written: {output}")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
