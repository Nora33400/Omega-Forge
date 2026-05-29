from omega_forge.core.task_queue import TaskQueue


def test_add_and_reload_task(tmp_path):
    path = tmp_path / "tasks.json"
    queue = TaskQueue(path)

    task = queue.add("Write tests", description="Protect the core", priority=1)

    assert task.title == "Write tests"
    assert task.status == "pending"
    assert queue.summary()["total"] == 1

    reloaded = TaskQueue(path)
    assert len(reloaded.tasks) == 1
    assert reloaded.tasks[0].title == "Write tests"


def test_set_task_status(tmp_path):
    path = tmp_path / "tasks.json"
    queue = TaskQueue(path)
    task = queue.add("Finish queue")

    updated = queue.set_status(task.id, "done")

    assert updated.status == "done"
    assert queue.summary()["done"] == 1
    assert len(updated.history) >= 2


def test_list_by_status(tmp_path):
    path = tmp_path / "tasks.json"
    queue = TaskQueue(path)
    done = queue.add("Done task")
    queue.add("Pending task")
    queue.set_status(done.id, "done")

    assert len(queue.list("done")) == 1
    assert len(queue.list("pending")) == 1
