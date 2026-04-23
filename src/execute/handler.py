import asyncio

from src.task_model.task import Task


class Handler:

    async def handle(self, task: Task) -> None:
        if task.status == "new":
            task.start()
            await asyncio.sleep(0.5)
            task.complete()
        elif task.status == "cancelled":
