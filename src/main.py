import asyncio
import logging
import sys

from src.execute.executor import TaskExecutor
from src.execute.handler import Handler
from src.receiver.collect_tasks import collect_tasks
from src.sources.generator_tasks_source import GeneratorTaskSource
from src.task_model.task import Task

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    stream=sys.stdout,
)


def print_tasks(title: str, tasks: list[Task]) -> None:
    print(f"\n=== {title} ({len(tasks)} tasks) ===")

    for i, task in enumerate(tasks, start=1):
        print(
            f"[{i}] id={task.id}, desc={task.description}, "
            f"priority={task.priority}, status={task.status}"
        )


async def demo_async_executor() -> None:
    print("=== Async Task Queue Demo ===")

    tasks = collect_tasks(GeneratorTaskSource(count=6))
    for task in tasks:
        task.status = "new"

    print_tasks("Before executor run", tasks)

    handler = Handler(processing_delay=0.2)

    async with TaskExecutor(handler=handler, worker_count=2) as executor:
        await executor.run(tasks)

    print_tasks("After processing", tasks)


def main() -> None:
    asyncio.run(demo_async_executor())


if __name__ == "__main__":
    main()
