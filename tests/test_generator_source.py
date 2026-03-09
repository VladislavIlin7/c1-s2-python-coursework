import pytest

from src.exception import InvalidCountException
from src.sources.generator_tasks_source import GeneratorTaskSource


def test_generator_basic():
    source = GeneratorTaskSource(count=3, start_id=1)
    tasks = source.get_tasks()

    assert len(tasks) == 3
    assert [t.id for t in tasks] == ["1", "2", "3"]


def test_generator_payload_sample():
    source = GeneratorTaskSource(count=2, payload_sample="x")
    tasks = source.get_tasks()

    assert all(t.payload == "x" for t in tasks)


def test_generator_negative():
    with pytest.raises(InvalidCountException):
        GeneratorTaskSource(count=-1)
