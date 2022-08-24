import os
from datetime import datetime, timezone
from typing import List

from src.models import MessageModel


class ClearDataFiles:
    def __init__(self, file: str):
        # Pasta de arquivo das conversas
        self.__folder_files = 'file_folder/'
        if not os.path.exists(self.__folder_files):
            os.mkdir(self.__folder_files)

        # Recebe os dados limpos
        self.__clean_data = self.__clear_data(file)

    def __clear_data(self, file: str) -> List[MessageModel]:
        """
        Limpa o arquivo com os dados
        :param file: arquivo com a exportação da conversa
        :return: retorna uma lista de dicionarios
        """
        data_return = []
        with open(f"{self.__folder_files}/{file}", "r", encoding="utf-8") as arquivo:
            for line in arquivo.readlines():
                line = line.strip('\n')

                # Verifica se a linha esta vazia
                if line.replace(' ',
                                '') == '' or ' ' in line or line == "\t" or 'saiu' in line or 'entrou usando o link' \
                        in line or 'Nem mesmo o WhatsApp pode ler ou ouvi-las. Toque para saber mais.' in line or \
                        'Você bloqueou esse contato' in line or 'Você desbloqueou esse contato.' in line:
                    continue

                try:
                    # Verifica se é do tipo data
                    datetime.strptime(line.split()[0], '%d/%m/%Y').date()
                except Exception:
                    # Caso de erro, verifica se a list esta vazia
                    if data_return:
                        # Adiciona concatena a ultima mensagem
                        data_return[-1].message += f" {line}"
                    continue

                # Tira a quebra de linha e separa em data, hora / contato, mensagem
                line = line.split('-', 1)
                # Remove os espaços da data / separa a mensagem do contato
                try:
                    line = line[0].split() + line[1].split(':', 1)
                except Exception as error:
                    print('dado não capturado', str(error), line, type(error))
                    continue

                data_return.append(MessageModel(phone=line[2][1:],
                                                date=datetime.strptime(f"{line[0]} {line[1]}", '%d/%m/%Y %H:%M'),
                                                message=line[-1].lower()[1:]))

        return data_return

    def filter_data(self, phone: str = None, date: str = None, message: str = None) -> List[MessageModel]:
        """
        Filtra objetivamente

        :param phone:
        :param date: filtra somente pro dia "dd/mm/YYYY"
        :param message: para encontrar dentro
        :return:
        """
        list_data = self.__clean_data

        if phone:
            list_data = [_ for _ in list_data if _.phone == phone]

        if date:
            date = datetime.fromisoformat(date + '0+00:00').astimezone(timezone.utc)
            list_data = [_ for _ in list_data if _.phone == date.date()]

        if message:
            list_data = [_ for _ in list_data if message in _.message]
        return list_data
