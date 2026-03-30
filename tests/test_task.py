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
    assert task.is_ready_to_start is True
    assert task.status_label == "Новая"
    assert task.age_seconds >= 0


def test_status_flow():
    task = Task("1", "test", 0, "new")

    task.start()
    assert task.status == "in_progress"

    task.complete()
    assert task.status == "completed"

    task.cancel()
    assert task.status == "cancelled"


def test_start_invalid_state():
    task = Task("1", "test", 0, "in_progress")

    with pytest.raises(InvalidTaskStatusException):
        task.start()


def test_complete_invalid_state():
    task = Task("1", "test", 0, "new")

    with pytest.raises(InvalidTaskStatusException):
        task.complete()


def test_cancel_invalid_state():
    task = Task("1", "test", 0, "in_progress")

    with pytest.raises(InvalidTaskStatusException):
        task.cancel()


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
