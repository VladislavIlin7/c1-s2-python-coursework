import json
from pathlib import Path

import pytest

from src.exception import InvalidTaskDataException, InvalidTaskItemException, InvalidTypeTaskDataException
from src.sources.file_tasks_source import FileTaskSource
from src.task_model.task import Task


def write_tasks_file(data, filename: str) -> Path:
    path = Path(__file__).with_name(filename)
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_file_basic():
    data = [
        {"id": "1", "payload": "a"},
        {"id": "2", "payload": "b"},
    ]
    path = write_tasks_file(data, "_test_tasks_basic.json")

    try:
        source = FileTaskSource(str(path))
        tasks = source.get_tasks()
    finally:
        path.unlink(missing_ok=True)

    assert len(tasks) == 2
    assert isinstance(tasks[0], Task)
    assert isinstance(tasks[1], Task)
    assert tasks[0].id == "1"
    assert tasks[0].description == "a"
    assert tasks[1].id == "2"
    assert tasks[1].description == "b"


def test_file_not_list():
    data = {"id": "1"}
    path = write_tasks_file(data, "_test_tasks_not_list.json")

    try:
        with pytest.raises(InvalidTaskDataException):
            FileTaskSource(str(path)).get_tasks()
    finally:
        path.unlink(missing_ok=True)


def test_file_missing_id():
    data = [{"payload": "x"}]
    path = write_tasks_file(data, "_test_tasks_missing_id.json")

    try:
        with pytest.raises(InvalidTaskItemException):
            FileTaskSource(str(path)).get_tasks()
    finally:
        path.unlink(missing_ok=True)


def test_file_item_not_dict():
    data = ["not a dict"]
    path = write_tasks_file(data, "_test_tasks_item_not_dict.json")

    try:
        with pytest.raises(InvalidTypeTaskDataException):
            FileTaskSource(str(path)).get_tasks()
    finally:
        path.unlink(missing_ok=True)
