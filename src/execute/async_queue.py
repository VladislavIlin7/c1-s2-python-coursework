import asyncio

from src.task_model.task import Task


class AsyncTaskQueue:
    """Асинхронная очередь для Task"""

    def __init__(self, maxsize: int = 0) -> None:
        """Создает очередь с ограничением размера"""
        self._queue: asyncio.Queue[Task] = asyncio.Queue(maxsize=maxsize)

    async def put(self, task: Task) -> None:
        """Добавляет Task в очередь"""
        if not isinstance(task, Task):
            raise TypeError("AsyncTaskQueue добавляет только Task")
        await self._queue.put(task)

    async def get(self) -> Task:
        """Возвращает следующую Task из очереди"""
        return await self._queue.get()

    async def join(self) -> None:
        """Ожидает завершения всех задач в очереди"""
        await self._queue.join()

    def task_done(self) -> None:
        """Отмечает текущую Task как обработанную"""
        self._queue.task_done()

    def qsize(self) -> int:
        """Возвращает количество Task в очереди"""
        return self._queue.qsize()
