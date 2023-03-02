from typing import List

from loguru import logger
from sqlalchemy import func

from config import Conector, Logger
from src.models import MessagesTable, DatesDto, NumberOfMessagesModel


class SearchInChatFilter(Logger):
    def __init__(self, id_file: int):
        super().__init__()
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

                phones = list({phone for phone, in query.all()})

                logger.info(f'Successfully extracted {len(phones)} phone(s)')

        except Exception as error:
            logger.error(error)
            raise error

        return phones

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

    # def extract_links(self, dates: DatesDto = DatesDto):
    #     """Extract links"""
    #     with Conector() as session:
    #         query = session.query(MessagesTable).filter(MessagesTable.id_file == self.__id_file)
    #
    #         if dates.start_date:
    #             query = query.filter(MessagesTable.date >= dates.start_date)
    #
    #         if dates.end_date:
    #             query = query.filter(MessagesTable.date <= dates.end_date)
    #
    #         list_phone_link = {}
    #
    #         for message in query:
    #             links = re.findall(r'(https?://\S+)', message.message)
    #
    #             list_phone_link = {}
    #
    #         logger.info(f'Successfully extracted {len(list_phone_link)} links')
    #
    #         print(list_phone_link)


if __name__ == '__main__':
    search = SearchInChatFilter(id_file=1)
    # quantidade_numeros = search.get_message_count_by_phone()
    # print(quantidade_numeros)
    # print(search.get_list_of_numbers())
    # print(search.group_or_privaty)
    # search.extract_links()

    # from dataclasses import dataclass
    #
    # @dataclass
    # class PhoneLinksModel:
    #     """PhoneLinksModel"""
    #     phone: str
    #     links: List[str]
    #
    #     def insert_link(self, links: List[str]):
    #         self.links.extend(links)
    #
    #
    # link = [PhoneLinksModel(phone='erickson', links=['123']), PhoneLinksModel(phone='gabriela', links=['456'])]
    #
    # for item in link:
    #     if item.phone == 'erickson':
    #         item.insert_link(['789'])
    # print(link)
