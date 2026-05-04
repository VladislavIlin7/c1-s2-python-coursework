import asyncio
import logging
from types import TracebackType
from typing import Iterable

from src.execute.async_queue import AsyncTaskQueue
from src.execute.handler_protocol import TaskHandler
from src.task_model.task import Task

logger = logging.getLogger(__name__)


class TaskExecutor:
    """Асинхронный исполнитель задач с пулом воркеров"""

    def __init__(self, handler: TaskHandler, worker_count: int = 1) -> None:
        """Создает executor с обработчиком и количеством воркеров"""
        if worker_count <= 0:
            raise ValueError("worker_count должен быть > 0")

        self._handler: TaskHandler = handler
        self._worker_count: int = worker_count
        self._queue: AsyncTaskQueue = AsyncTaskQueue(maxsize=worker_count)
        self._workers: list[asyncio.Task[None]] = []

    async def __aenter__(self) -> "TaskExecutor":
        """Запускает worker-задачи при входе в async with"""
        if self._workers:
            raise RuntimeError("TaskExecutor уже запущен")

        self._workers = [
            asyncio.create_task(self._worker())
            for _ in range(self._worker_count)
        ]
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Останавливает worker при выходе из async with"""
        for worker in self._workers:
            worker.cancel()

        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()

    async def _worker(self) -> None:
        """Обрабатывает Task из очереди до отмены worker-задачи"""
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
        """Добавляет переданные Task в очередь и ожидает их обработки"""
        if not self._workers:
            raise RuntimeError("TaskExecutor должен использоваться через async with")

        for task in tasks:
            await self._queue.put(task)

        await self._queue.join()
