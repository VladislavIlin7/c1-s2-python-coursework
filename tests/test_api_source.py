from src.sources.api_tasks_source import ApiTaskSource
from src.task_model.task import Task


def test_api_basic():
    source = ApiTaskSource("http://test")
    tasks = source.get_tasks()

    assert len(tasks) == 3
    assert isinstance(tasks[0], Task)
    assert tasks[1].id == "2"
    assert tasks[1].description == "api task 2"
    assert tasks[1].priority == 0
    assert tasks[1].status == "new"
