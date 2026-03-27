from __future__ import annotations

from datetime import datetime
from typing import Any

from src.exception import (
    InvalidTaskIdException,
    InvalidTaskDescriptionException,
    InvalidTaskPriorityException,
    InvalidTaskStatusException,
    InvalidTaskCreatedAtException,
)


class TaskIdDescriptor:
    """Дескриптор для id задачи"""

    def __init__(self, storage_name: str) -> None:
        self.storage_name = storage_name

    def __get__(self, instance: Any, owner: type | None = None) -> str | TaskIdDescriptor:
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidTaskIdException()
        setattr(instance, self.storage_name, value.strip())


class TaskDescriptionDescriptor:
    """Дескриптор для описания задачи"""

    def __init__(self, storage_name: str) -> None:
        self.storage_name = storage_name

    def __get__(self, instance: Any, owner: type | None = None) -> str | TaskDescriptionDescriptor:
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidTaskDescriptionException()
        setattr(instance, self.storage_name, value.strip())


class TaskPriorityDescriptor:
    """Дескриптор для приоритета задачи"""

    def __init__(self, storage_name: str) -> None:
        self.storage_name = storage_name

    def __get__(self, instance: Any, owner: type | None = None) -> int | TaskPriorityDescriptor:
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int) or value < 0:
            raise InvalidTaskPriorityException()
        setattr(instance, self.storage_name, value)


class TaskStatusDescriptor:
    """Дескриптор для статуса задачи"""

    ALLOWED_STATUSES = {"new", "in_progress", "done", "cancelled"}

    def __init__(self, storage_name: str) -> None:
        self.storage_name = storage_name

    def __get__(self, instance: Any, owner: type | None = None) -> str | TaskStatusDescriptor:
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, str) or value not in self.ALLOWED_STATUSES:
            raise InvalidTaskStatusException()
        setattr(instance, self.storage_name, value)


class TaskCreatedAtDescriptor:
    """Дескриптор для времени создания задачи"""

    def __init__(self, storage_name: str) -> None:
        self.storage_name = storage_name

    def __get__(self, instance: Any, owner: type | None = None) -> datetime | TaskCreatedAtDescriptor:
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, datetime):
            raise InvalidTaskCreatedAtException()
        setattr(instance, self.storage_name, value)


class StatusLabelDescriptor:
    """Non-data descriptor для человекочитаемой метки статуса"""

    def __get__(self, instance: Any, owner: type | None = None) -> str | StatusLabelDescriptor:
        if instance is None:
            return self

        mapping = {
            "new": "Новая",
            "in_progress": "В работе",
            "done": "Завершена",
            "cancelled": "Отменена",
        }
        return mapping[instance.status]