from datetime import datetime, timezone
from stop_words import stopwordsnltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from typing import List
import string
import re
import os


class ClearDataFiles:
    def __init__(self):
        # Pasta de arquivo das conversas
        self.__folder_files = 'file_folder/'
        if not os.path.exists(self.__folder_files):
            os.mkdir(self.__folder_files)

    def clear_data(self, file: str, id_file: int) -> list:
        """
        Limpa o arquivo com os dados
        :param id_file: id referente ao arquivo no banco
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
                        'Você bloqueou esse contato' in line or 'Você desbloqueou esse contato.' in line or \
                        line is None:
                    continue

                try:
                    # Verifica se é do tipo data
                    datetime.strptime(line.split()[0], '%d/%m/%Y').date()
                except Exception:
                    # Caso de erro, verifica se a list esta vazia
                    # if data_return:
                    #     try:
                    #         if line:
                    #             texto = list(data_return[-1])
                    #             texto[-1] = f"{texto} {str(line)}"
                    #
                    #             print(texto)
                    #
                    #             data_return[-1] = tuple(texto)
                    #
                    #     except Exception as error:
                    #         print(f"[{data_return[-1]}] [{str(line)}] [{error}]")
                    #         continue

                    continue

                # Tira a quebra de linha e separa em data, hora / contato, mensagem
                line = line.split('-', 1)
                # Remove os espaços da data / separa a mensagem do contato
                try:
                    line = line[0].split() + line[1].split(':', 1)
                except Exception:
                    print('dado não capturado')
                    continue

                # Cria um dicionário com os dados e adiciona na lista
                data_return.append((
                    id_file,
                    line[2][1:],
                    datetime.strptime(f"{line[0]} {line[1]}", '%d/%m/%Y %H:%M'),
                    line[-1].lower()[1:]
                ))

        return data_return


if __name__ == '__main__':
    classe = ClearDataFiles().clear_data("conversa", 1)
    numero = 'Paulo Mota'
    # [print(_[-1]) for _ in classe]
