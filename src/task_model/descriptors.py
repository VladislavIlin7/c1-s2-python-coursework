from __future__ import annotations

from datetime import datetime
from typing import Any

from src.exception import InvalidTaskIdException, InvalidTaskDescriptionException, InvalidTaskPriorityException, \
    InvalidTaskStatusException, InvalidTaskCreatedAtException


class BaseStorageDescriptor:
    """Базовый дескриптор с автоматическим вычислением storage_name"""

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.storage_name = f"_{name}"

    def __get__(self, instance: Any, owner: type | None = None):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)


class TaskIdDescriptor(BaseStorageDescriptor):
    """Дескриптор для id задачи"""

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidTaskIdException()
        setattr(instance, self.storage_name, value.strip())


class TaskDescriptionDescriptor(BaseStorageDescriptor):
    """Дескриптор для описания задачи"""

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidTaskDescriptionException()
        setattr(instance, self.storage_name, value.strip())


class TaskPriorityDescriptor(BaseStorageDescriptor):
    """Дескриптор для приоритета задачи"""

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int) or value < 0:
            raise InvalidTaskPriorityException()
        setattr(instance, self.storage_name, value)


class TaskStatusDescriptor(BaseStorageDescriptor):
    """Дескриптор для статуса задачи"""

    ALLOWED_STATUSES = {"new", "in_progress", "completed", "cancelled"}

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, str) or value not in self.ALLOWED_STATUSES:
            raise InvalidTaskStatusException(value)
        setattr(instance, self.storage_name, value)


class TaskCreatedAtDescriptor(BaseStorageDescriptor):
    """Дескриптор для времени создания задачи"""

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, datetime):
            raise InvalidTaskCreatedAtException()
        setattr(instance, self.storage_name, value)


class StatusLabelDescriptor:
    """Non-data descriptor для русского статуса"""

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name

    def __get__(self, instance: Any, owner: type | None = None):
        if instance is None:
            return self

        mapping = {
            "new": "Новая",
            "in_progress": "В работе",
            "completed": "Завершена",
            "cancelled": "Отменена",
        }
        return mapping[instance.status]
