import json

import pytest

from src.exception import InvalidTaskDataException, InvalidTaskItemException, InvalidTypeTaskDataException
from src.sources.file_tasks_source import FileTaskSource
from src.task_model.task import Task


def test_file_basic(tmp_path):
    data = [
        {"id": "1", "payload": "a"},
        {"id": "2", "payload": "b"},
    ]
    path = tmp_path / "tasks.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    source = FileTaskSource(str(path))
    tasks = source.get_tasks()

    assert len(tasks) == 2
    assert isinstance(tasks[0], Task)
    assert isinstance(tasks[1], Task)
    assert tasks[0].id == "1"
    assert tasks[0].description == "a"
    assert tasks[1].id == "2"
    assert tasks[1].description == "b"


def test_file_not_list(tmp_path):
    data = {"id": "1"}
    path = tmp_path / "tasks.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(InvalidTaskDataException):
        FileTaskSource(str(path)).get_tasks()


def test_file_missing_id(tmp_path):
    data = [{"payload": "x"}]
    path = tmp_path / "tasks.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(InvalidTaskItemException):
        FileTaskSource(str(path)).get_tasks()

def test_file_item_not_dict(tmp_path):
    data = ["not a dict"]
    path = tmp_path / "tasks.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(InvalidTypeTaskDataException):
        FileTaskSource(str(path)).get_tasks()