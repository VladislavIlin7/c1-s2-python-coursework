from dataclasses import dataclass
from typing import Any


@dataclass()
class Task:
    """
    Описывает одну задачу

    :param id: Уникальный идентификатор задачи
    :param payload: Данные задачи которые нужно обработать
    """

    id: str
    payload: Any
