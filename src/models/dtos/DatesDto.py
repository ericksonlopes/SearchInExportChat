from dataclasses import dataclass
from datetime import datetime


@dataclass
class DatesDto:
    """Messages datas transfer object."""
    start_date: datetime = None
    end_date: datetime = None

    def __call__(self, *args, **kwargs) -> dict:
        return self.__dict__
