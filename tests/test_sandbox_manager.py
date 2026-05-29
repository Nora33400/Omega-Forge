import sys

import pytest

from omega_forge.core.sandbox_manager import SandboxManager


def test_create_and_destroy_session(tmp_path):
    manager = SandboxManager(root=tmp_path / "sandboxes")

    session = manager.create_session()

    assert session.status == "created"
    assert session.path.exists()

    destroyed = manager.destroy_session(session.id)

    assert destroyed.status == "destroyed"
    assert not session.path.exists()


def test_run_command_success(tmp_path):
    manager = SandboxManager(root=tmp_path / "sandboxes")
    session = manager.create_session()

    result = manager.run_command(
        session.id,
        [sys.executable, "-c", "print('omega')"],
    )

    assert result.ok is True
    assert result.exit_code == 0
    assert "omega" in result.stdout
    assert session.status == "stopped"


def test_run_command_failure(tmp_path):
    manager = SandboxManager(root=tmp_path / "sandboxes")
    session = manager.create_session()

    result = manager.run_command(
        session.id,
        [sys.executable, "-c", "import sys; sys.exit(7)"],
    )

    assert result.ok is False
    assert result.exit_code == 7
    assert session.status == "stopped"


def test_create_session_copies_workspace(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "hello.txt").write_text("world", encoding="utf-8")

    manager = SandboxManager(root=tmp_path / "sandboxes")
    session = manager.create_session(source_workspace=source)

    assert (session.path / "hello.txt").read_text(encoding="utf-8") == "world"


def test_run_command_with_relative_cwd(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    subdir = source / "subdir"
    subdir.mkdir()
    (subdir / "marker.txt").write_text("inside", encoding="utf-8")

    manager = SandboxManager(root=tmp_path / "sandboxes")
    session = manager.create_session(source_workspace=source)

    result = manager.run_command(
        session.id,
        [sys.executable, "-c", "from pathlib import Path; print(Path('marker.txt').read_text())"],
        cwd="subdir",
    )

    assert result.ok is True
    assert "inside" in result.stdout


def test_cwd_cannot_escape_sandbox(tmp_path):
    manager = SandboxManager(root=tmp_path / "sandboxes")
    session = manager.create_session()

    with pytest.raises(ValueError):
        manager.run_command(session.id, [sys.executable, "-c", "print('bad')"], cwd=tmp_path)
