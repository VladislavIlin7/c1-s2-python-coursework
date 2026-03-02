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