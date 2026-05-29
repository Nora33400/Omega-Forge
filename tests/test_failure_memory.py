from omega_forge.core.failure_memory import FailureMemory, error_signature


def test_record_failure(tmp_path):
    memory = FailureMemory(tmp_path / "failures.json")

    entry = memory.record_failure(
        "ModuleNotFoundError: No module named requests",
        task_title="Build API",
        project_type="python",
        template_name="api",
    )

    assert entry.status == "unresolved"
    assert entry.signature
    assert memory.summary()["total"] == 1
    assert memory.summary()["unresolved"] == 1


def test_repeated_failure_detection(tmp_path):
    memory = FailureMemory(tmp_path / "failures.json")

    first = memory.record_failure(
        "ModuleNotFoundError: No module named requests",
        project_type="python",
        template_name="api",
    )
    second = memory.record_failure(
        "ModuleNotFoundError: No module named requests",
        project_type="python",
        template_name="api",
    )

    assert second.id == first.id
    assert second.status == "repeated"
    assert memory.summary()["total"] == 1
    assert memory.summary()["repeated"] == 1


def test_mark_resolved(tmp_path):
    memory = FailureMemory(tmp_path / "failures.json")
    entry = memory.record_failure("NameError: name x is not defined")

    resolved = memory.mark_resolved(entry.id, "Defined x before usage")

    assert resolved.status == "resolved"
    assert resolved.repair_result == "Defined x before usage"
    assert memory.summary()["resolved"] == 1


def test_find_similar(tmp_path):
    memory = FailureMemory(tmp_path / "failures.json")
    entry = memory.record_failure(
        "FileNotFoundError: config.json",
        project_type="python",
        template_name="cli",
    )

    found = memory.find_similar(
        "FileNotFoundError: config.json",
        project_type="python",
        template_name="cli",
    )

    assert found is not None
    assert found.id == entry.id


def test_save_and_reload(tmp_path):
    path = tmp_path / "failures.json"
    memory = FailureMemory(path)
    entry = memory.record_failure("ImportError: cannot import name App")
    memory.mark_resolved(entry.id, "Fixed import path")

    reloaded = FailureMemory(path)

    assert reloaded.summary()["total"] == 1
    assert reloaded.entries[0].status == "resolved"
    assert reloaded.entries[0].repair_result == "Fixed import path"


def test_error_signature_is_stable():
    first = error_signature("ModuleNotFoundError", template_name="api", project_type="python")
    second = error_signature("  modulenotfounderror  ", template_name="API", project_type="PYTHON")

    assert first == second
    assert len(first) == 16
