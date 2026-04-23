import asyncio
from typing import Iterable

from src.execute.async_queue import AsyncTaskQueue
from src.execute.handler_protocol import TaskHandler
from src.task_model.task import Task


class TaskExecutor:
    def __init__(self, handler: TaskHandler, worker_count: int = 1) -> None:
        self._handler: TaskHandler = handler
        self._worker_count: int = worker_count
        self._queue: AsyncTaskQueue = AsyncTaskQueue()

    async def submit(self, tasks: Iterable[Task]) -> None:
        await self._queue.put_many(tasks)


    async def _worker(self) -> None:
        while True:
            task = await self._queue.get()
            try:
                await self._handler.handle(task)
            except Exception as e:
                print(e)
            finally:
                self._queue.task_done()

    async def run(self, tasks: Iterable[Task]) -> None:
        await self.submit(tasks)

        workers = [asyncio.create_task(self._worker()) for _ in range(self._worker_count)]


        for worker in workers:
            worker.cancel()

        await asyncio.gather(*workers, return_exceptions=True)
