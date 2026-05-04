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


def test_async_queue_invalid_item():
    async def run():
        queue = AsyncTaskQueue()
        with pytest.raises(TypeError):
            await queue.put("bad")

    asyncio.run(run())
