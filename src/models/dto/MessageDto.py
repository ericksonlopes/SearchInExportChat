from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class MessageDto:
    """Messages data transfer object."""
    phone: str = None
    start_date: datetime = None
    end_date: datetime = None
    message: str = None
    list_phone: List[str] = None

    def __call__(self, *args, **kwargs) -> dict:
        return self.__dict__
