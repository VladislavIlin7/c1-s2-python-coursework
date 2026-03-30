from typing import Protocol, runtime_checkable

from src.task_model.task import Task


@runtime_checkable
class TaskMapperSource(Protocol):
    """
    Контракт для источников задач

    Каждый источник должен реализовать метод get_tasks
    """

    def get_tasks(self) -> list[Task]:
        """
        Возвращает список объектов Task

        :return: Список задач
        """
        ...
