from typing import Iterator, Iterable

from src.exception import InvalidTaskSourceException, InvalidIntervalException
from src.task_model.task import Task


class TaskQueue:
    def __init__(self, tasks: Iterable[Task]) -> None:
        self._tasks = list(tasks)
        for task in self._tasks:
            if not isinstance(task, Task):
                raise TypeError("TaskQueue принимает только Task объекты")

    def __iter__(self) -> Iterator[Task]:
        return iter(self._tasks)

    def filter_by_status(self, status: str) -> Iterator[Task]:
        for task in self._tasks:
            if task.status == status:
                yield task

    def filter_by_priority(self, min_priority: int | None = None, max_priority: int | None = None) -> Iterator[Task]:
        if min_priority is not None and max_priority is not None and min_priority > max_priority:
            raise InvalidIntervalException

        for task in self._tasks:
            if min_priority is not None and task.priority < min_priority:
                continue
            if max_priority is not None and task.priority > max_priority:
                continue
            yield task

    def add_task(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError("TaskQueue принимает только Task объекты")
        self._tasks.append(task)

    def __len__(self) -> int:
        return len(self._tasks)

    def __repr__(self) -> str:
        return f"TaskQueue(tasks={len(self._tasks)})"
