from src.exception import InvalidTaskSourceException
from src.protocols.task_source import TaskSource
from src.task_model.task import Task


def validate_source(source: TaskSource) -> list[Task]:
    if not isinstance(source, TaskSource):
        raise InvalidTaskSourceException
    return source.get_tasks()
