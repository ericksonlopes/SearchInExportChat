from loguru import logger

from config import setup_logger
from sqlalchemy_config import Conector
from src.clear_file import ClearDataFile
from src.models import MessagesTable, InfoMessagesTable, FilesTable


class AddMessages(ClearDataFile):
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
                    path=self.path_file
                )
                session.add(file)
                session.flush()

                # return id file inserted
                self.__id_file = file.id

            logger.info(f'Successfully added file {self.name_file}({self.path_file}) to database, id: {self.__id_file}')
        except Exception as error:
            logger.error(error)
            raise error

    def __add_message(self) -> None:
        """add messages in database"""
        try:
            with Conector() as session:
                # add messages
                session.add_all(map(lambda message: MessagesTable(
                    phone=message.phone,
                    message=message.message,
                    id_file=self.__id_file
                ), self.messages))

                # add info messages
                session.add_all(map(lambda message: InfoMessagesTable(
                    message=message.message,
                    id_file=self.__id_file
                ), self.info_messages))

            logger.info(f'Successfully added messages to database ({len(self.messages)} itens)')
        except Exception as error:
            logger.error(error)
            raise error
