from datetime import datetime

from src.exception import InvalidTaskStatusException
from src.task_model.descriptors import TaskIdDescriptor, TaskDescriptionDescriptor, TaskPriorityDescriptor, \
    TaskStatusDescriptor, TaskCreatedAtDescriptor, StatusLabelDescriptor


class Task:
    """Модель задачи с валидацией через дескрипторы."""

    id = TaskIdDescriptor()
    description = TaskDescriptionDescriptor()
    priority = TaskPriorityDescriptor()
    status = TaskStatusDescriptor()
    created_at = TaskCreatedAtDescriptor()

    status_label = StatusLabelDescriptor()

    def __init__(self,
                 id: str,
                 description: str,
                 priority: int = 0,
                 status: str = "new",
                 created_at: datetime | None = None) -> None:
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
        self.created_at = created_at or datetime.now()

    @property
    def is_ready_to_start(self) -> bool:
        return self.status == "new"

    @property
    def is_in_progress(self) -> bool:
        return self.status == "in_progress"

    @property
    def is_completed(self) -> bool:
        return self.status == "completed"

    @property
    def age_seconds(self) -> float:
        return (datetime.now() - self.created_at).total_seconds()

    def start(self) -> None:
        if self.is_ready_to_start:
            self.status = "in_progress"
        else:
            raise InvalidTaskStatusException(self.status)

    def complete(self) -> None:
        if self.is_in_progress:
            self.status = "completed"
        else:
            raise InvalidTaskStatusException(self.status)

    def cancel(self) -> None:
        if self.is_completed:
            self.status = "cancelled"
        else:
            raise InvalidTaskStatusException(self.status)
