from omega_forge.core.patch_plan import (
    PatchPlan,
    PatchTarget,
    build_patch_plan_from_failure,
    infer_patch_strategy,
)


def test_infer_patch_strategy_common_errors():
    assert infer_patch_strategy("ModuleNotFoundError: No module named requests") == "add_dependency"
    assert infer_patch_strategy("FileNotFoundError: config.json") == "create_missing_file"
    assert infer_patch_strategy("NameError: name x is not defined") == "create_missing_symbol"
    assert infer_patch_strategy("ImportError: cannot import name App") == "fix_import"
    assert infer_patch_strategy("Invalid path configured") == "fix_path"
    assert infer_patch_strategy("Configuration missing") == "repair_configuration"
    assert infer_patch_strategy("Temporary timeout") == "retry_generation"
    assert infer_patch_strategy("Unexpected unknown failure") == "manual_review"


def test_build_patch_plan_from_failure_adds_target():
    plan = build_patch_plan_from_failure(
        failure_id="failure-1",
        error_text="ModuleNotFoundError: No module named requests",
        artifact_path="requirements.txt",
    )

    assert plan.failure_id == "failure-1"
    assert plan.strategy == "add_dependency"
    assert plan.status == "pending"
    assert plan.targets[0].path == "requirements.txt"


def test_patch_plan_mark_status():
    plan = PatchPlan(strategy="manual_review", rationale="Needs human review")

    plan.mark("approved")

    assert plan.status == "approved"


def test_patch_plan_add_target():
    plan = PatchPlan(strategy="fix_import", rationale="Broken import")

    target = plan.add_target("omega_forge/core/app.py", reason="Import failure", must_exist=True)

    assert target.path == "omega_forge/core/app.py"
    assert target.must_exist is True
    assert plan.targets == [target]


def test_patch_plan_roundtrip():
    plan = PatchPlan(
        failure_id="failure-1",
        strategy="create_missing_file",
        rationale="Missing config file",
        targets=[PatchTarget(path="config.json", reason="Missing file")],
        metadata={"source": "test"},
    )

    restored = PatchPlan.from_dict(plan.to_dict())

    assert restored.id == plan.id
    assert restored.failure_id == "failure-1"
    assert restored.strategy == "create_missing_file"
    assert restored.targets[0].path == "config.json"
    assert restored.metadata["source"] == "test"
