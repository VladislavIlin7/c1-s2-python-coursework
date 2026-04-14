import pytest

from src.exception import InvalidIntervalException, InvalidTaskSourceException
from src.queue.task_queue import TaskQueue
from src.task_model.task import Task


def test_queue_iteration_and_len():
    tasks = [
        Task("1", "task 1", 1, "new"),
        Task("2", "task 2", 3, "completed"),
    ]
    queue = TaskQueue(tasks)

    assert len(queue) == 2
    assert list(queue) == tasks


def test_queue_iteration_repeatable():
    tasks = [
        Task("1", "task 1", 1, "new"),
        Task("2", "task 2", 3, "completed"),
    ]
    queue = TaskQueue(tasks)

    first = list(queue)
    second = list(queue)

    assert first == second


def test_filter_by_status():
    tasks = [
        Task("1", "task 1", 1, "new"),
        Task("2", "task 2", 2, "in_progress"),
        Task("3", "task 3", 3, "new"),
    ]
    queue = TaskQueue(tasks)

    filtered = list(queue.filter_by_status("new"))

    assert [t.id for t in filtered] == ["1", "3"]


def test_filter_by_priority_range():
    tasks = [
        Task("1", "task 1", 0, "new"),
        Task("2", "task 2", 2, "new"),
        Task("3", "task 3", 5, "new"),
    ]
    queue = TaskQueue(tasks)

    filtered = list(queue.filter_by_priority(min_priority=1, max_priority=4))

    assert [t.id for t in filtered] == ["2"]


def test_filter_by_priority_min_only():
    tasks = [
        Task("1", "task 1", 0, "new"),
        Task("2", "task 2", 2, "new"),
    ]
    queue = TaskQueue(tasks)

    filtered = list(queue.filter_by_priority(min_priority=1))

    assert [t.id for t in filtered] == ["2"]


def test_filter_by_priority_max_only():
    tasks = [
        Task("1", "task 1", 0, "new"),
        Task("2", "task 2", 3, "new"),
    ]
    queue = TaskQueue(tasks)

    filtered = list(queue.filter_by_priority(max_priority=1))

    assert [t.id for t in filtered] == ["1"]


def test_filter_by_priority_invalid_interval():
    tasks = [
        Task("1", "task 1", 1, "new"),
    ]
    queue = TaskQueue(tasks)

    with pytest.raises(InvalidIntervalException):
        list(queue.filter_by_priority(min_priority=5, max_priority=1))


def test_filter_invalid_task_source():
    queue = TaskQueue([Task("1", "task 1", 1, "new"), "bad"])

    with pytest.raises(TypeError):
        list(queue.filter_by_status("new"))


def test_add_task_and_repr():
    queue = TaskQueue([])

    queue.add_task(Task("1", "task 1", 1, "new"))

    assert len(queue) == 1
    assert repr(queue) == "TaskQueue(cached=1)"
