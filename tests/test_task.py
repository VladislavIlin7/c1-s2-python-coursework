from datetime import datetime

import pytest

from src.task_model.task import Task
from src.exception import InvalidTaskStatusException, InvalidTaskIdException, InvalidTaskDescriptionException, \
    InvalidTaskPriorityException, InvalidTaskCreatedAtException


def test_create_task():
    created_at = datetime(2024, 1, 1, 12, 0, 0)
    task = Task("1", "test task", 1, "new", created_at=created_at)

    assert task.id == "1"
    assert task.description == "test task"
    assert task.priority == 1
    assert task.status == "new"
    assert task.created_at == created_at
    assert task.is_ready is True
    assert task.is_done is False
    assert task.status_label == "Новая"
    assert task.age_seconds >= 0


def test_status_flow():
    task = Task("1", "test", 0, "new")

    task.start()
    assert task.status == "in_progress"

    task.complete()
    assert task.status == "done"
    assert task.is_done is True

    task.cancel()
    assert task.status == "cancelled"


def test_status_change_to_invalid_value_raises_error():
    task = Task("1", "test", 0, "new")

    with pytest.raises(InvalidTaskStatusException):
        task.status = "invalid"


def test_task_creation_invalid_id():
    with pytest.raises(InvalidTaskIdException):
        Task("", "desc", 0, "new")


def test_task_creation_invalid_description():
    with pytest.raises(InvalidTaskDescriptionException):
        Task("1", "", 0, "new")


def test_task_creation_invalid_priority():
    with pytest.raises(InvalidTaskPriorityException):
        Task("1", "desc", -1, "new")


def test_task_creation_invalid_created_at():
    with pytest.raises(InvalidTaskCreatedAtException):
        Task("1", "desc", 0, "new", created_at="wrong")
