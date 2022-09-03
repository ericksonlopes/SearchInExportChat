import datetime
from dataclasses import dataclass
from typing import List

from src.models import MessageModel


@dataclass
class FilterMessagesModel:
    """Filter messages by type and severity."""
    phone: str = None
    start_date: datetime = None
    end_date: datetime = None
    message: str = None

    def __call__(self, messages: List[MessageModel]) -> List[MessageModel]:
        """Filter messages by phone, date and message."""
        if self.phone is not None:
            messages = filter(lambda message: message.phone == self.phone, messages)

        if (self.start_date and self.end_date) is not None:
            messages = filter(lambda message: self.start_date <= message.date <= self.end_date, messages)

        if self.message is not None:
            messages = filter(lambda message: self.message.upper() in message.message.upper(), messages)

        return list(messages)
