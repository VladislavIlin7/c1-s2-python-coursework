import json
import logging

from src.exception import InvalidTaskDataException, InvalidTypeTaskDataException, InvalidTaskItemException
from src.task_model.task import Task

logger = logging.getLogger(__name__)


class FileTaskSource:
    """
    Читает задачи из json файла
    """

    def __init__(self, path: str) -> None:
        """
        Сохраняет путь к файлу

        :param path: Путь к json файлу с задачами
        """
        self._path = path

    def get_tasks(self) -> list[Task]:
        """
        Читает файл и возвращает список задач

        :return: Список задач прочитанных из файла
        """
        logger.info("Чтение задач из файла %s", self._path)
        with open(self._path, encoding="utf-8") as f:
            data = json.load(f)
            logger.info("Файл успешно прочитан")

        if not isinstance(data, list):
            logger.error("Файл JSON должен содержать массив задач")
            raise InvalidTaskDataException

        tasks: list[Task] = []
        for item in data:
            if not isinstance(item, dict):
                logger.error("Каждый элемент должен быть в виде словаря")
                raise InvalidTypeTaskDataException

            task_id = item.get("id")
            payload = item.get("payload")
            priority = item.get("priority", 0)
            status = item.get("status", "new")

            if task_id is None:
                logger.error("Задачи должны иметь свой id")
                raise InvalidTaskItemException

            tasks.append(
                Task(
                    id=str(task_id),
                    description=str(payload),
                    priority=priority,
                    status=status,
                )
            )

        return tasks
