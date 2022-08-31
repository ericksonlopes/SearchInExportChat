import os
import re
from datetime import datetime
from typing import List

from src.models import MessageModel, InfoMessageModel


class ClearDataFiles:
    def __init__(self, pathfile: str):
        self.__file = pathfile
        self.__messages: List[MessageModel] = []
        self.__info_messages: List[InfoMessageModel] = []

        self.__read_file()

    @property
    def messages(self) -> List[MessageModel]:
        return self.__messages

    @property
    def info_messages(self) -> List[InfoMessageModel]:
        return self.__info_messages

    @property
    def file(self) -> str:
        return self.__file

    def __read_file(self) -> None:
        if not os.path.exists(self.__file):
            raise FileNotFoundError(f'File {self.__file} not found')

        with open(self.__file, encoding='utf-8') as file:
            for item in file.readlines():
                find = re.findall(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*?): (.*)', item, re.MULTILINE)

                if find:
                    message = MessageModel(phone=find[0][1], message=' '.join(find[0][2].split()),
                                           date=datetime.strptime(f"{find[0][0]}", '%d/%m/%Y %H:%M'))
                    self.messages.append(message)
                    continue

                find2 = re.findall(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*)', item, re.MULTILINE)

                if find2:
                    info_message = InfoMessageModel(date=datetime.strptime(f"{find2[0][0]}", '%d/%m/%Y %H:%M'),
                                                    message=find2[0][1])
                    self.info_messages.append(info_message)
                    continue

                self.messages[-1].message += f" {' '.join(item.split())}"
