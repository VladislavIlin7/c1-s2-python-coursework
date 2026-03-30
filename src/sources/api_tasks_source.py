import logging

from src.exception import InvalidTaskItemException
from src.task_model.task import Task

logger = logging.getLogger(__name__)


class ApiTaskSource:
    """
    Имитирует внешний api
    """

    def __init__(self, base_url: str, path: str = "/tasks") -> None:
        """
        Сохраняет параметры api

        :param base_url: Базовый адрес api
        :param path: Путь до ресурса с задачами
        """
        self._base_url = base_url
        self._path = path

    def get_tasks(self) -> list[Task]:
        """
        Возвращает задачи как будто получены из api

        :return: Список задач полученных из api
        """
        logger.info("Имитация запроса к API")
        # url = self._basic_url + "/" + self._path

        data = [
            {"id": "1", "payload": "api task 1", "priority": 1, "status": "new"},
            {"id": "2", "payload": "api task 2", "priority": 3, "status": "in_progress"},
            {"id": "3", "payload": "api task 3", "priority": 5, "status": "done"},
        ]
        tasks: list[Task] = []

        for item in data:
            task_id = item.get("id")
            payload = item.get("payload")

            if task_id is None:
                logger.error("Задачи должны иметь свой id")
                raise InvalidTaskItemException

            tasks.append(
                Task(
                    id=str(task_id),
                    description=str(payload),
                    priority=0,
                    status="new",
                )
            )

        return tasks
