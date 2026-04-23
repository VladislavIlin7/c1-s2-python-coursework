from typing import Protocol

from src.task_model.task import Task


class TaskHandler(Protocol):
    async def handle(self, task: Task) -> None:
        ...
