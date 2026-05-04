import asyncio
import logging

from src.task_model.task import Task

logger = logging.getLogger(__name__)


class Handler:
    """Асинхронный обработчик Task"""

    def __init__(self, processing_delay: float = 0.5) -> None:
        """Создает обработчик с задержкой обработки"""
        self._processing_delay = processing_delay

    async def handle(self, task: Task) -> None:
        try:
            if task.status == "new":
                task.start()
                await asyncio.sleep(self._processing_delay)
                task.complete()
            elif task.status == "in_progress":
                await asyncio.sleep(self._processing_delay)
                task.complete()
            elif task.status == "cancelled":
                logger.info("Задача %s уже отменена", task.id)
            else:
                logger.info("Задача %s пропущена со статусом %s", task.id, task.status)
        except Exception as e:
            logger.error("Ошибка при обработке задачи %s: %s", task.id, e)
