import asyncio

from src.execute.handler import Handler
from src.task_model.task import Task


def test_handler_completes_new_task():
    async def run():
        handler = Handler(processing_delay=0)
        task = Task("1", "task 1", 1, "new")
        await handler.handle(task)
        assert task.status == "completed"
    asyncio.run(run())


def test_handler_skips_cancelled_task():
    async def run():
        handler = Handler(processing_delay=0)
        task = Task("1", "task 1", 1, "cancelled")
        await handler.handle(task)
        assert task.status == "cancelled"
    asyncio.run(run())


def test_handler_skips_non_new_task():
    async def run():
        handler = Handler(processing_delay=0)
        task = Task("1", "task 1", 1, "in_progress")
        await handler.handle(task)
        assert task.status == "completed"

    asyncio.run(run())
