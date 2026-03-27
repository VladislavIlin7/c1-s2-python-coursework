import logging
import sys
from pathlib import Path

from src.receiver.collect_tasks import collect_tasks
from src.sources.api_tasks_source import ApiTaskSource
from src.sources.file_tasks_source import FileTaskSource
from src.sources.generator_tasks_source import GeneratorTaskSource

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    stream=sys.stdout
)


def print_tasks(title: str, tasks: list) -> None:
    print(f"\n=== {title} ({len(tasks)} задач) ===")

    for i, task in enumerate(tasks, start=1):
        print(f"[{i}] id={task.id}, desc={task.description}, "
              f"priority={task.priority}, status={task.status}, "
              f"label={task.status_label}")


def main() -> None:
    print("=== Проверка системы задач ===")

    # Генератор
    generator = GeneratorTaskSource(count=2)
    gen_tasks = collect_tasks(generator)
    print_tasks("Generator", gen_tasks)

    # API (заглушка)
    api = ApiTaskSource("http://example.com")
    api_tasks = collect_tasks(api)
    print_tasks("API", api_tasks)

    # Файл
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / "tasks.json"
    file_source = FileTaskSource(str(file_path))
    file_tasks = collect_tasks(file_source)
    print_tasks("File", file_tasks)


if __name__ == "__main__":
    main()