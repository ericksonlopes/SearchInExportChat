import re
from datetime import datetime
from typing import List

from src.models import MessageModel, InfoMessageModel


class ClearDataFiles:
    def __init__(self, file: str):
        self.__file = file

    with open('file_folder/conversa.txt', encoding='utf-8') as file:
        list_message: List[MessageModel] = []
        list_info_message: List[InfoMessageModel] = []

        for item in file.readlines():
            find = re.findall(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*?): (.*)', item, re.MULTILINE)

            if find:
                message = MessageModel(phone=find[0][1], message=' '.join(find[0][2].split()),
                                       date=datetime.strptime(f"{find[0][0]}", '%d/%m/%Y %H:%M'))
                list_message.append(message)
                continue

            find2 = re.findall(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*)', item, re.MULTILINE)

            if find2:
                info_message = InfoMessageModel(date=datetime.strptime(f"{find2[0][0]}", '%d/%m/%Y %H:%M'),
                                                message=find2[0][1])
                list_info_message.append(info_message)
                continue

            list_message[-1].message += f" {' '.join(item.split())}"

        # [print(item) for item in list_message]
        # print(len(list_message))
        print(list(filter(lambda x: x.phone == '@erickson.lds', list_message)))


if __name__ == '__main__':
    ClearDataFiles('conversa.txt')
