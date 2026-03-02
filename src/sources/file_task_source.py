import json

from src.exception import InvalidTaskDataException, InvalidTypeTaskDataException, InvalidTaskItemException
from src.task_model.task import Task


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
        """
        with open(self._path, encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise InvalidTaskDataException

        tasks: list[Task] = []
        for item in data:
            if not isinstance(item, dict):
                raise InvalidTypeTaskDataException

            task_id = item.get("id")
            payload = item.get("payload")

            if task_id is None:
                raise InvalidTaskItemException

            tasks.append(Task(task_id, payload))

        return tasks
