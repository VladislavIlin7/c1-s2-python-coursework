import asyncio
import logging
from typing import Iterable

from src.execute.async_queue import AsyncTaskQueue
from src.execute.handler_protocol import TaskHandler
from src.task_model.task import Task

logger = logging.getLogger(__name__)


class TaskExecutor:
    """Запускает обработку Task одновременно с подключаемым асинхронным обработчиком"""

    def __init__(self, handler: TaskHandler, worker_count: int = 1) -> None:
        if worker_count <= 0:
            raise ValueError("worker_count должен быть > 0")

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
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Ошибка при обработке задачи %s", task.id)
            finally:
                self._queue.task_done()

    async def run(self, tasks: Iterable[Task]) -> None:
        await self.submit(tasks)

        workers = [
            asyncio.create_task(self._worker())
            for _ in range(self._worker_count)
        ]

        await self._queue.join()

        for worker in workers:
            worker.cancel()

        await asyncio.gather(*workers, return_exceptions=True)
