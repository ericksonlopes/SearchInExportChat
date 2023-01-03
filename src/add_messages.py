from dataclasses import dataclass
from typing import List, Any

from loguru import logger

from config import setup_logger
from sqlalchemy_config import Conector
from src.clear_file import BaseClearDataFile
from src.models import InfoMessagesTable, FilesTable, MessagesTable


class AddMessages(BaseClearDataFile):
    def __init__(self, pathfile: str):
        super().__init__(pathfile=pathfile)
        setup_logger()

        self.__id_file: int = 0
        self.__insert_file()
        self.__add_message()

    def __insert_file(self) -> None:
        """insert file in database"""
        try:
            with Conector() as session:
                file = FilesTable(
                    name=self.name_file,
                    path=self.path_file,
                    # type=self.type_file
                )
                session.add(file)
                session.flush()

                # return id file inserted
                self.__id_file = file.id

            logger.info(f'Successfully added file {self.name_file}({self.path_file}) to database, id: {self.__id_file}')
        except Exception as error:
            logger.error(error)
            raise error

    def __adapter_that_adds_id_file(self, list_data: List[Any], type_model: dataclass) -> map:
        """adapter data"""
        return map(lambda data: type_model(
            **data.__dict__,
            **{"id_file": self.__id_file}
        ), list_data)

    def __add_message(self) -> None:
        """add messages in database"""
        try:
            with Conector() as session:
                # add messages
                session.add_all(self.__adapter_that_adds_id_file(self.messages, MessagesTable))

                # add info messages
                session.add_all(self.__adapter_that_adds_id_file(self.info_messages, InfoMessagesTable))

            logger.info(f'Successfully added messages to database '
                        f'({len(self.messages)} messages and {len(self.info_messages)} info messages)')

        except Exception as error:
            logger.error(error)
            raise error
