from __future__ import annotations

from datetime import datetime

from src.task_model.descriptors import (
    TaskIdDescriptor,
    TaskDescriptionDescriptor,
    TaskPriorityDescriptor,
    TaskStatusDescriptor,
    TaskCreatedAtDescriptor,
    StatusLabelDescriptor,
)


class Task:
    """Модель задачи с валидацией через дескрипторы."""

    id = TaskIdDescriptor("_id")
    description = TaskDescriptionDescriptor("_description")
    priority = TaskPriorityDescriptor("_priority")
    status = TaskStatusDescriptor("_status")
    created_at = TaskCreatedAtDescriptor("_created_at")

    status_label = StatusLabelDescriptor()

    def __init__(
        self,
        id: str,
        description: str,
        priority: int = 0,
        status: str = "new",
        created_at: datetime | None = None,
    ) -> None:
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
        self.created_at = created_at or datetime.now()

    @property
    def is_ready(self) -> bool:
        return self.status == "new"

    @property
    def is_done(self) -> bool:
        return self.status == "done"

    @property
    def age_seconds(self) -> float:
        return (datetime.now() - self.created_at).total_seconds()

    def start(self) -> None:
        self.status = "in_progress"

    def complete(self) -> None:
        self.status = "done"

    def cancel(self) -> None:
        self.status = "cancelled"