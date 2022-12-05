from typing import List

from loguru import logger
from sqlalchemy import func

from config import setup_logger
from sqlalchemy_config import Conector
from src.models import MessagesTable, DatesDto, NumberOfMessagesModel


class SearchInChatFilter:
    def __init__(self, id_file: int):
        setup_logger()
        self.__id_file: int = id_file

    @property
    def group_or_privaty(self) -> str:
        """Return group or private"""
        try:
            len_phones = len(self.get_list_of_numbers())
            if len_phones > 2:
                result = 'group'

            elif len_phones == 2:
                result = 'private'
            else:
                result = 'unknown'

        except Exception as error:
            logger.error(error)
            raise error

        logger.info(f'{self.__id_file} is {result}')

        return result

    def get_list_of_numbers(self, dates: DatesDto = DatesDto) -> List[str]:
        """Get list of numbers"""
        try:
            with Conector() as conector:
                query = conector.query(MessagesTable.phone).filter(MessagesTable.id_file == self.__id_file)
                if dates.start_date:
                    query = query.filter(MessagesTable.date >= dates.start_date)

                if dates.end_date:
                    query = query.filter(MessagesTable.date <= dates.end_date)

                phones = query.all()

                logger.info(f'Successfully extracted {len(phones)} phone(s)')

        except Exception as error:
            logger.error(error)
            raise error

        return list({phone for phone, in phones})

    def get_message_count_by_phone(self, dates: DatesDto = DatesDto) -> List[NumberOfMessagesModel]:
        """Count messages"""
        with Conector() as session:
            query = session.query(MessagesTable).filter(MessagesTable.id_file == self.__id_file)

            if dates.start_date:
                query = query.filter(MessagesTable.date >= dates.start_date)

            if dates.end_date:
                query = query.filter(MessagesTable.date <= dates.end_date)

            query = query.group_by(MessagesTable.phone).with_entities(MessagesTable.phone,
                                                                      func.count(MessagesTable.message))

            return list(map(lambda message: NumberOfMessagesModel(phone=message[0], quantity=message[1]), query))
