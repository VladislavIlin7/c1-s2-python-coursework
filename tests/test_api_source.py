from src.sources.api_tasks_source import ApiTaskSource
from src.task_model.task import Task


def test_api_basic():
    source = ApiTaskSource("http://test")
    tasks = source.get_tasks()

    assert len(tasks) == 2
    assert isinstance(tasks[0], Task)
    assert tasks[1] == Task(id="2", payload="api task 2")