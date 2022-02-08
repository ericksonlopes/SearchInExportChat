from stop_words import stopwordsnltk
from collections import Counter
from datetime import datetime
import string
import re
import os

from wordcloud import WordCloud
import matplotlib.pyplot as plt


def clear_data(file: str) -> list:
    data_return = []
    with open(file, "r", encoding="utf-8") as arquivo:
        for line in arquivo.readlines():
            line = line.strip('\n')

            # Verifica se a linha esta vazia
            if line.replace(' ', '') == '' or ' ' in line or line == "\t" or 'saiu' in line or 'entrou usando o link' \
                    in line or 'Nem mesmo o WhatsApp pode ler ou ouvi-las. Toque para saber mais.' in line:
                continue

            try:
                try:
                    # Verifica se é do tipo data
                    datetime.strptime(line.split()[0], '%d/%m/%Y').date()
                except Exception:
                    # Verifica se é do tipo data
                    datetime.strptime(line.split()[0][:-1], '%m/%d/%y').date()

            except Exception:
                # Caso de erro, verifica se a list esta vazia
                if data_return:
                    # Adiciona concatena a ultima mensagem
                    data_return[-1]['message'] += f" {line}"
                continue

            # Tira a quebra de linha e separa em data, hora / contato, mensagem
            line = line.split('-', 1)
            # Remove os espaços da data / separa a mensagem do contato
            try:
                line = line[0].split() + line[1].split(':', 1)
            except Exception:
                continue

            # Cria um dicionário com os dados e adiciona na lista
            data_return.append({
                "phone": line[2][1:],
                "date": datetime.strptime(f"{line[0]} {line[1]}", '%d/%m/%Y %H:%M'),
                "message": line[-1].lower()
            })
    return data_return


class SearchInExportChat:

    def __init__(self, file: str):
        if not os.path.exists('file_folder'):
            # cria a pasta
            os.mkdir('file_folder')

        # Recebe os dados limpos
        self.data_return = clear_data(file)

    def extract_list_phones(self) -> list:
        """
        Função retorna todos os números que enviaram mensagem na conversa
        """

        list_phones = list({item['phone'] for item in self.data_return})

        list_return = [{'phone': item} for item in list_phones]

        return list_return

    def extract_message_phone(self, phone: str) -> list:
        """
        Função retorna uma lista com todas as mensagens de um determinado número
        """
        return [item['message'][1:] for item in self.data_return if item['phone'] == phone]

    def extract_data_phones(self, phone: str = None) -> list:
        """
        Função retorna toda a informação encontrada de um número na conversa
        """

        if phone:
            return [item for item in self.data_return if item['phone'] == phone]
        else:
            return self.data_return

    def count_messages_number(self, phone: str = None) -> int:
        """
        Retorna a quantidade de mensagens
        :param phone:
        :return:
        """
        if phone:
            return len(self.data_return)
        else:
            return len([_ for _ in self.data_return if _['phone'] == phone])

    def extract_links_in_message(self, phone: str = None) -> list:
        list_message = []

        midia_file = 0

        # Adiciona todas as mensagens em uma lista
        for item in self.extract_data_phones(phone):
            if item['message'].replace(' ', '') != '<arquivodemídiaoculto>':
                list_message.append(item['message'])
            else:
                # captura a quantidade de arquivos de midia enviado
                midia_file += 1

        # Cria uma lista com todas as palavras separadas por espaço
        str_message = ' '.join(list_message)

        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, str_message)

        return [x[0] for x in url]

    def search_text_in_message(self, text: str, phone: str = None) -> list:
        """
        Procura o texto especificado nas mensagens
        :param text:
        :param phone:
        :return:
        """
        if phone:
            return [item for item in self.data_return if text in item['message'] and item['phone'] == phone]
        else:
            return [item for item in self.data_return if text in item['message']]

    def word_occurrence_counter(self, phone: str, remove_punctuation: bool = False) -> dict:
        """
        Retorna uma lista de ocorrencias de todas as palavras enviadas pelo número especificado
        """
        list_message, midia_file = [], 0

        # Adiciona todas as mensagens em uma lista
        for item in self.extract_data_phones(phone):
            if item['message'].replace(' ', '') != '<arquivodemídiaoculto>':
                list_message.append(item['message'])
            else:
                # captura a quantidade de arquivos de midia enviado
                midia_file += 1

        # Cria uma lista com todas as palavras separadas por espaço
        str_message = ' '.join(list_message)

        # Remove a pontuação
        if remove_punctuation:
            for item in string.punctuation:
                str_message = str_message.replace(item, '')

        # Separa a string por espaços para formar uma lista
        str_message = str_message.split()

        # retira as stopwords
        str_message = [item for item in str_message if item not in stopwordsnltk]

        # Realiza a da lista contagem com o pandas
        str_dict = dict(Counter(str_message))

        # Junta o dicionario com outro(s)
        str_dict = {**{"Arquivos de midia": midia_file}, **str_dict}
        return str_dict

    def word_cloud(self, phone: str = None) -> None:
        list_message, midia_file = [], 0

        # Adiciona todas as mensagens em uma lista
        for item in self.extract_data_phones(phone):
            if item['message'].replace(' ', '') != '<arquivodemídiaoculto>':
                list_message.append(item['message'])
            else:
                # captura a quantidade de arquivos de midia enviado
                midia_file += 1

        # Cria uma lista com todas as palavras separadas por espaço
        str_message = ' '.join(list_message)

        # Separa a string por espaços para formar uma lista
        str_message = str_message.split()

        # retira as stopwords
        str_message = [item for item in str_message if item not in stopwordsnltk]

        wordcloud = WordCloud().generate(' '.join(str_message))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.savefig('teste.png')


if __name__ == '__main__':
    cafe_mm = SearchInExportChat('file_folder/conversa')
    numero = 'Paulo Mota'

    # print(cafe_mm.extract_list_phones())
    # print(cafe_mm.extract_message_phone(numero))
    # print(cafe_mm.extract_data_phones(numero))
    # print(cafe_mm.extract_data_phones())
    # print(cafe_mm.word_occurrence_counter(numero, remove_punctuation=False))
    # print(cafe_mm.word_occurrence_counter(numero, remove_punctuation=True))
    # print(cafe_mm.extract_links_in_message(numero))
    # print(cafe_mm.count_messages_number(numero))
    # [print(_) for _ in cafe_mm.search_text_in_message('asterisco')]
    # [print(_) for _ in cafe_mm.search_text_in_message('celular', 'Paulo Mota')]
    cafe_mm.word_cloud('+55 31 8950-6741')

    # Quantidade de mensagens enviadas
    # Colocar links para o telefone e ter uma tela com as estatisticas dele

    # desistalar o pandas
