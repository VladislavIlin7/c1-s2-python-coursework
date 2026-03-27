from datetime import datetime

import pytest

from src.task_model.task import Task
from src.exception import (
    InvalidTaskCreatedAtException,
    InvalidTaskDescriptionException,
    InvalidTaskIdException,
    InvalidTaskPriorityException,
    InvalidTaskStatusException,
)


def test_valid_task_creation():
    created_at = datetime(2024, 1, 1, 10, 0, 0)
    task = Task("123", "valid description", 10, "in_progress", created_at=created_at)

    assert task.id == "123"
    assert task.description == "valid description"
    assert task.priority == 10
    assert task.status == "in_progress"
    assert task.created_at == created_at


def test_empty_id_raises_error():
    with pytest.raises(InvalidTaskIdException):
        Task("", "desc", 0, "new")


def test_blank_description_raises_error():
    with pytest.raises(InvalidTaskDescriptionException):
        Task("1", "", 0, "new")


def test_non_integer_priority_raises_error():
    with pytest.raises(InvalidTaskPriorityException):
        Task("1", "desc", "high", "new")


def test_invalid_status_raises_error():
    with pytest.raises(InvalidTaskStatusException):
        Task("1", "desc", 0, "wrong")


def test_invalid_created_at_raises_error():
    with pytest.raises(InvalidTaskCreatedAtException):
        Task("1", "desc", 0, "new", created_at="not datetime")