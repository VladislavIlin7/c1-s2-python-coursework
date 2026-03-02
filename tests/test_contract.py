import pytest

from src.exception import InvalidTaskSourceException
from src.receiver.collect_tasks import collect_tasks
from src.sources.generator_tasks_source import GeneratorTaskSource


def test_validate_ok():
    source = GeneratorTaskSource(1)
    tasks = collect_tasks(source)

    assert len(tasks) == 1


def test_validate_bad():
    class Bad:
        pass

    with pytest.raises(InvalidTaskSourceException):
        bet = Bad()
        collect_tasks(bet)