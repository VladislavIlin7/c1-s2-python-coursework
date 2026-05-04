from typing import Protocol

from src.task_model.task import Task


class TaskHandler(Protocol):
    """Протокол асинхронного обработчика Task"""

    async def handle(self, task: Task) -> None:
        """Обрабатывает переданную Task"""
        ...
