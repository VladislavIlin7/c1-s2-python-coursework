import logging
from typing import Any

from src.exception import InvalidCountException
from src.task_model.task import Task

logger = logging.getLogger(__name__)


class GeneratorTaskSource:
    """
    Генератор задач
    """

    def __init__(self, count: int, start_id=1, payload_sample: Any = None) -> None:
        """
        Создает генератор задач

        :param count: Количество задач
        :param start_id: Начальный id задачи
        :param payload_sample: Данные которые будут использоваться как payload
        """
        if count < 0:
            logger.error("Количество генерируемых задач не может быть < 0")
            raise InvalidCountException

        self._count = count
        self._start_id = start_id
        self._payload_sample = payload_sample

    def get_tasks(self) -> list[Task]:
        """
        Генерирует список задач и возвращает его

        :return: Список сгенерированных задач
        """
        logger.info("Генерация %s задач", self._count)

        tasks: list[Task] = []
        for i in range(self._count):
            task_id = self._start_id + i
            if self._payload_sample is None:
                payload = f"generated task {task_id}"
            else:
                payload = self._payload_sample
            tasks.append(
                Task(
                    id=str(task_id),
                    description=str(payload),
                    priority=0,
                    status="new",
                )
            )

        return tasks
