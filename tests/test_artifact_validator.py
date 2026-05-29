from omega_forge.core.artifact_validator import ArtifactValidator


def test_validator_rejects_missing_artifact(tmp_path):
    result = ArtifactValidator().validate(tmp_path, tmp_path / "missing.py")

    assert result.ok is False
    assert result.path is not None
    assert result.checks == []
    assert "does not exist" in result.errors[0]


def test_validator_accepts_valid_python_file(tmp_path):
    artifact = tmp_path / "valid.py"
    artifact.write_text("def healthcheck():\n    return {'status': 'ok'}\n", encoding="utf-8")

    result = ArtifactValidator().validate(tmp_path, artifact)

    assert result.ok is True
    assert "exists" in result.checks
    assert "python_syntax" in result.checks
    assert result.errors == []


def test_validator_rejects_invalid_python_file(tmp_path):
    artifact = tmp_path / "invalid.py"
    artifact.write_text("def broken(:\n    pass\n", encoding="utf-8")

    result = ArtifactValidator().validate(tmp_path, artifact)

    assert result.ok is False
    assert "exists" in result.checks
    assert any("Python syntax error" in error for error in result.errors)


def test_validator_accepts_markdown_file(tmp_path):
    artifact = tmp_path / "generated.md"
    artifact.write_text("# Generated\n", encoding="utf-8")

    result = ArtifactValidator().validate(tmp_path, artifact)

    assert result.ok is True
    assert result.checks == ["exists"]
    assert result.errors == []


def test_validator_rejects_none_path(tmp_path):
    result = ArtifactValidator().validate(tmp_path, None)

    assert result.ok is False
    assert result.path is None
    assert result.errors == ["No artifact path was provided."]
