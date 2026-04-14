from typing import Iterable, Iterator

from src.exception import InvalidIntervalException
from src.task_model.task import Task


class ReplayableTasks:
    """Ленивая обёртка с кэшированием и повторной итерацией"""

    def __init__(self, tasks: Iterable[Task]) -> None:
        self._source = iter(tasks)
        self._cache: list[Task] = []
        self._exhausted = False

    def __iter__(self) -> Iterator[Task]:
        index = 0

        while True:
            if index < len(self._cache):
                yield self._cache[index]
                index += 1
                continue

            if self._exhausted:
                return

            try:
                item = next(self._source)
            except StopIteration:
                self._exhausted = True
                return

            self._cache.append(item)
            yield item
            index += 1

    def append(self, item: Task) -> None:
        """Добавление задачи в кэш"""
        self._cache.append(item)

    @property
    def cached_count(self) -> int:
        """Количество кэшированных задач"""
        return len(self._cache)


class TaskQueue:
    """Очередь задач с ленивой фильтрацией"""

    def __init__(self, tasks: Iterable[Task]) -> None:
        self._tasks = ReplayableTasks(tasks)

    def __iter__(self) -> Iterator[Task]:
        for task in self._tasks:
            if not isinstance(task, Task):
                raise TypeError("TaskQueue принимает только Task объекты")
            yield task

    def filter_by_status(self, status: str) -> Iterator[Task]:
        """Фильтр по статусу"""
        for task in self:
            if task.status == status:
                yield task

    def filter_by_priority(
            self,
            min_priority: int | None = None,
            max_priority: int | None = None,
    ) -> Iterator[Task]:
        """Фильтр по диапазону приоритета"""
        if min_priority is not None and max_priority is not None and min_priority > max_priority:
            raise InvalidIntervalException

        for task in self:
            if min_priority is not None and task.priority < min_priority:
                continue
            if max_priority is not None and task.priority > max_priority:
                continue
            yield task

    def add_task(self, task: Task) -> None:
        """Добавление задачи"""
        if not isinstance(task, Task):
            raise TypeError("TaskQueue принимает только Task объекты")
        self._tasks.append(task)

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def __repr__(self) -> str:
        return f"TaskQueue(cached={self._tasks.cached_count})"
