from typing import Any


class ApplicationException(Exception):
    """Базовый класс исключений"""

    def __init__(self, message: str) -> None:
        super().__init__(f'{message}')


class InvalidTaskSourceException(ApplicationException):
    def __init__(self):
        super().__init__("Некорректный источник задач, не соблюдается TaskSource")


class InvalidCountException(ApplicationException):
    def __init__(self):
        super().__init__("Количество генерируемых задач не может быть < 0")


class InvalidTaskDataException(ApplicationException):
    def __init__(self):
        super().__init__("Файл JSON должен содержать массив задач")


class InvalidTypeTaskDataException(ApplicationException):
    def __init__(self):
        super().__init__("Каждый элемент должен быть в виде словаря")


class InvalidTaskItemException(ApplicationException):
    def __init__(self):
        super().__init__("Задачи должны иметь свой id")


class InvalidTaskIdException(ApplicationException):
    def __init__(self) -> None:
        super().__init__("Идентификатор задачи должен быть непустой строкой")


class InvalidTaskDescriptionException(ApplicationException):
    def __init__(self) -> None:
        super().__init__("Описание задачи должно быть непустой строкой")


class InvalidTaskPriorityException(ApplicationException):
    def __init__(self) -> None:
        super().__init__("Приоритет задачи должен быть целым числом >= 0")

class InvalidTaskStatusException(ApplicationException):
    def __init__(self, status: Any) -> None:
        super().__init__(f"Статус задачи имеет недопустимое значение: {status}")


class InvalidTaskCreatedAtException(ApplicationException):
    def __init__(self) -> None:
        super().__init__("Время создания задачи должно быть объектом datetime")
