from pathlib import Path

from src.receiver.collect_tasks import collect_tasks
from src.sources.api_tasks_source import ApiTaskSource
from src.sources.file_tasks_source import FileTaskSource
from src.sources.generator_tasks_source import GeneratorTaskSource


def main() -> None:
    # Генератор
    generator = GeneratorTaskSource(count=2)
    gen_tasks = collect_tasks(generator)
    print("Generator:", gen_tasks)

    # API заглушка
    api = ApiTaskSource("http://example.com")
    api_tasks = collect_tasks(api)
    print("API:", api_tasks)

    # Файл
    base_dir = Path(__file__).resolve().parent  # папка src
    file_path = base_dir / "tasks.json"
    file_source = FileTaskSource(str(file_path))
    file_tasks = collect_tasks(file_source)
    print("File:", file_tasks)


if __name__ == "__main__":
    main()
