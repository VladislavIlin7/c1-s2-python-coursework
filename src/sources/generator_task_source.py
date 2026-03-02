from typing import Any

from src.task_model.task import Task


class GeneratorTaskSource:
    """
    Генератор задач
    """

    def __init__(self, count: int, start_id=1, payload_sample: Any = None):

        if count < 0:
            raise

        self._count = count
        self._start_id = start_id
        self._payload_sample = payload_sample

    def get_tasks(self) -> list[Task]:
        tasks: list[Task] = []
        for i in range(self._count):
            task_id = self._start_id + i
            if self._payload_sample is None:
                payload = f"generated task {task_id}"
            else:
                payload = self._payload_sample
            tasks.append(Task(task_id, payload))
        return tasks
