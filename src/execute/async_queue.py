import asyncio
from typing import Iterable

from src.task_model.task import Task


class AsyncTaskQueue:
    def __init__(self) -> None:
        self._queue: asyncio.Queue[Task] = asyncio.Queue()



    async def put(self, task: Task) -> None:
        await self._queue.put(task)

    async def put_many(self, tasks: Iterable[Task]) -> None:
        for task in tasks:
            if not isinstance(task, Task):
                raise TypeError("В очередь можно добавлять только Task ")
            await self._queue.put(task)


    async def get(self) -> Task:
        return await self._queue.get()


    def task_done(self) -> None:
        self._queue.task_done()

    async def join(self) -> None:
        await self._queue.join()

    def qsize(self) -> int:
        return self._queue.qsize()