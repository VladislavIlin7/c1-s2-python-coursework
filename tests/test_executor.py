import asyncio

import pytest

from src.execute.executor import TaskExecutor
from src.task_model.task import Task


class RecordingHandler:
    def __init__(self) -> None:
        self.handled: list[str] = []

    async def handle(self, task: Task) -> None:
        self.handled.append(task.id)
        task.start()
        task.complete()


class FailingHandler:
    def __init__(self) -> None:
        self.handled: list[str] = []

    async def handle(self, task: Task) -> None:
        self.handled.append(task.id)
        if task.id == "2":
            raise RuntimeError("boom")
        task.start()
        task.complete()


def test_executor_run_completes_tasks():
    async def run():
        tasks = [
            Task("1", "task 1", 1, "new"),
            Task("2", "task 2", 2, "new"),
        ]
        handler = RecordingHandler()
        executor = TaskExecutor(handler, worker_count=2)

        async with executor:
            await executor.run(tasks)

        assert set(handler.handled) == {"1", "2"}
        assert [task.status for task in tasks] == ["completed", "completed"]

    asyncio.run(run())


def test_executor_invalid_worker_count():
    with pytest.raises(ValueError):
        TaskExecutor(RecordingHandler(), worker_count=0)


def test_executor_logs_error_and_continues(caplog):
    async def run():
        tasks = [
            Task("1", "task 1", 1, "new"),
            Task("2", "task 2", 2, "new"),
            Task("3", "task 3", 3, "new"),
        ]
        handler = FailingHandler()
        executor = TaskExecutor(handler, worker_count=2)

        with caplog.at_level("ERROR"):
            async with executor:
                await executor.run(tasks)

        assert set(handler.handled) == {"1", "2", "3"}
        assert tasks[0].status == "completed"
        assert tasks[1].status == "new"
        assert tasks[2].status == "completed"
        assert "Ошибка при обработке задачи 2" in caplog.text

    asyncio.run(run())


def test_executor_requires_context_manager():
    async def run():
        executor = TaskExecutor(RecordingHandler())

        with pytest.raises(RuntimeError):
            await executor.run([Task("1", "task 1", 1, "new")])

    asyncio.run(run())
