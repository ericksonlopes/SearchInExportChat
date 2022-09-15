import datetime
from dataclasses import dataclass
from typing import List

from src.models import MessageModel, MessageDto


@dataclass
class FilterMessagesModel(MessageDto):
    """Filter messages by type and severity."""

    def __call__(self, messages: List[MessageModel]) -> List[MessageModel]:
        """Filter messages"""

        if self.phone is not None:
            messages = filter(lambda message: message.phone == self.phone, messages)

        if (self.start_date and self.end_date) is not None:
            messages = filter(lambda message: self.start_date <= message.date <= self.end_date, messages)

        if self.message is not None:
            messages = filter(lambda message: self.message.upper() in message.message.upper(), messages)

        if self.list_phone is not None:
            messages = filter(lambda message: message.phone in self.list_phone, messages)

        return list(messages)
