from stopwords import stopwordsnltk
from datetime import datetime
import pandas as pd
import string
import re


def clear_data(file: str):
    data_return = []
    with open(file, "r", encoding="utf-8") as arquivo:
        for line in arquivo.readlines():
            line = line.strip('\n')

            # Verifica se a linha esta vazia
            if line.replace(' ',
                            '') == '' or "joined using this group's invite link" in line or ' ' in line or line == "\t" or 'saiu' in line or 'entrou usando o link' in line:
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
            line = line[0].split() + line[1].split(':', 1)
            # Cria um dicionário com os dados e adiciona na lista
            data_return.append({
                # "id": line[2].replace(' ', ''),
                "id": line[2][1:],
                "date": f"{line[0]} {line[1]}",
                "message": line[-1].lower()
            })
    return data_return


class SearchInExportChat:

    def __init__(self, file: str):
        self.data_return = clear_data(file)

    def extract_list_numbers(self):
        """
        Função retorna todos os números que enviaram mensagem na conversa
        """
        return list({item['id'] for item in self.data_return})

    def extract_data_number(self, phone: str = None) -> list:
        """
        Função retorna toda a informação encontrada de um número na conversa
        """

        if phone:
            return [item for item in self.data_return if item['id'] == phone]
        else:
            return self.data_return

    def extract_message_number(self, phone: str):
        """
        Função retorna uma lista com todas as mensagens de um determinado número
        """
        return [item['message'] for item in self.data_return if item['id'] == phone]

    def extract_links_in_message(self, phone: str = None):
        list_message = []

        midia_file = 0

        # Adiciona todas as mensagens em uma lista
        for item in self.extract_data_number(phone):
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

    def word_occurrence_counter(self, phone: str, remove_punctuation: bool = False):
        """
        Retorna uma lista de ocorrencias de todas as palavras enviadas pelo número especificado
        """

        list_message = []

        midia_file = 0

        # Adiciona todas as mensagens em uma lista
        for item in self.extract_data_number(phone):
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
        str_series = pd.Series(str_message).value_counts()

        # Gera um dicionario com o Series gerado
        str_dict = str_series.to_dict()

        # Junta o dicionario com outro(s)
        str_dict = {**{"Arquivos de midia": midia_file}, **str_dict}
        return str_dict


if __name__ == '__main__':
    cafe_mm = SearchInExportChat('file_folder/conversa.txt')

    numero = 'Paulo Mota'
    # print(cafe_mm.extract_list_numbers())
    # print(cafe_mm.extract_message_number(numero))
    # print(cafe_mm.extract_data_number(numero))
    # print(cafe_mm.word_occurrence_counter(numero,  remove_punctuation=False))
    # print(cafe_mm.extract_links_in_message(numero))

