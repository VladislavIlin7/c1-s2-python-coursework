import asyncio

import pytest

from src.execute.async_queue import AsyncTaskQueue
from src.task_model.task import Task


def test_async_queue_put_get():
    async def run():
        queue = AsyncTaskQueue()
        task = Task("1", "task 1", 1, "new")
        await queue.put(task)
        assert queue.qsize() == 1
        result = await queue.get()
        queue.task_done()
        assert result == task
        assert queue.qsize() == 0
    asyncio.run(run())


def test_async_queue_put_many():
    async def run():
        queue = AsyncTaskQueue()
        tasks = [
            Task("1", "task 1", 1, "new"),
            Task("2", "task 2", 2, "new"),
        ]
        await queue.put_many(tasks)
        first = await queue.get()
        second = await queue.get()
        queue.task_done()
        queue.task_done()
        assert [first.id, second.id] == ["1", "2"]

    asyncio.run(run())


def test_async_queue_invalid_item():
    async def run():
        queue = AsyncTaskQueue()
        with pytest.raises(TypeError):
            await queue.put("bad")

    asyncio.run(run())
