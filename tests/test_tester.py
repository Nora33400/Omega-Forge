from omega_forge.agents.tester import TesterAgent


def test_tester_scores_complete_workspace(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "omega_forge" / "core").mkdir(parents=True)
    (tmp_path / "omega_forge" / "agents").mkdir(parents=True)
    (tmp_path / "tests").mkdir()

    result = TesterAgent().run({"root": str(tmp_path)})

    assert result.success is True
    assert result.data["score"] == 4
    assert result.data["max_score"] == 4
    assert all(result.data["checks"].values())


def test_tester_scores_incomplete_workspace(tmp_path):
    (tmp_path / "docs").mkdir()

    result = TesterAgent().run({"root": str(tmp_path)})

    assert result.success is True
    assert result.data["score"] < result.data["max_score"]
    assert result.data["checks"]["docs"] is True
    assert result.data["checks"]["core"] is False
