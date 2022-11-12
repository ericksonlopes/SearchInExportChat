from dataclasses import dataclass
from typing import List

from loguru import logger

from config import setup_logger
from src.models import MessageModel, MessageDto


@dataclass
class FilterMessagesModel(MessageDto):
    """Filter messages by type and severity."""
    setup_logger()

    def __call__(self, messages: List[MessageModel]) -> List[MessageModel]:
        """Filter messages"""
        try:
            if self.phone:
                messages = filter(lambda message: message.phone == self.phone, messages)

            if (self.start_date and self.end_date) is not None:
                messages = filter(lambda message: self.start_date <= message.date <= self.end_date, messages)

            if self.message:
                messages = filter(lambda message: self.message.upper() in message.message.upper(), messages)

            if self.list_phone:
                messages = filter(lambda message: message.phone in self.list_phone, messages)

            result = list(messages)
            logger.info(f'Successfully filtered {len(result)} messages')
            logger.info(f'Filtered by {self.__dict__}')
        except Exception as error:
            logger.error(f'Error filtering messages: {error}')
            raise error

        return result
