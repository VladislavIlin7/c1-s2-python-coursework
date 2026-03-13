import logging

from src.exception import InvalidTaskSourceException
from src.protocols.task_source import TaskSource
from src.task_model.task import Task

logger = logging.getLogger(__name__)


def collect_tasks(source: TaskSource) -> list[Task]:
    """
    Проверяет источник и получает задачи

    :param source: Объект реализующий контракт TaskSource
    :return: Список задач полученных из источника
    """
    if not isinstance(source, TaskSource):
        logger.error("Некорректный источник задач, не соблюдается TaskSource")
        raise InvalidTaskSourceException
    return source.get_tasks()
