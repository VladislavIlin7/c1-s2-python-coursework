from typing import Iterator

from src.task_model.task import Task


class TaskQueue:
    def __init__(self, tasks: list[Task]) -> None:
        self._tasks = list(tasks)

    def __iter__(self) -> Iterator[Task]:
        return iter(self._tasks)

    def filter_by_status(self, status: str) -> Iterator[Task]:
        for task in self._tasks:
            if task.status == status:
                yield task

    def filter_by_priority(self, min_priority: int | None = None, max_priority: int | None = None) -> Iterator[Task]:
        for task in self._tasks:
            if min_priority is not None and task.priority < min_priority:
                continue
            if max_priority is not None and task.priority > max_priority:
                continue
            yield task
