from datetime import datetime, timezone
from stop_words import stopwordsnltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import string
import re
import os


class ClearDataFiles:
    def __init__(self, file: str):
        # Pasta de arquivo das conversas
        self.__folder_files = 'file_folder/'
        if not os.path.exists(self.__folder_files):
            os.mkdir(self.__folder_files)

        # Recebe os dados limpos
        self.__clean_data = self.__clear_data(file)

    def __clear_data(self, file: str) -> list:
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
                    "message": line[-1].lower()[1:]
                })
        return data_return

    def filter_data(self, phone: str = None, date: str = None, message: str = None) -> list:
        """
        Filtra objetivamente

        :param phone:
        :param date: filtra somente pro dia "dd/mm/YYYY"
        :param message: para encontrar dentro
        :return:
        """
        list_data = self.__clean_data

        if phone:
            list_data = [_ for _ in list_data if _["phone"] == phone]

        if date:
            date = datetime.fromisoformat(date + '0+00:00').astimezone(timezone.utc)
            list_data = [_ for _ in list_data if _["date"].date() == date.date()]

        if message:
            list_data = [_ for _ in list_data if message in _["message"]]
        return list_data


class SearchInExportChat(ClearDataFiles):
    def __init__(self, file: str):
        super().__init__(file)
        self.__type_chat: str
        self.__folder_word_cloud = 'word_cloud/'

        if not os.path.exists(self.__folder_word_cloud):
            os.mkdir(self.__folder_word_cloud)

        # Verifica se é uma conversa ou grupo
        if len(self.list_phones()) > 2:
            self.__type_chat = 'grupo'
        else:
            self.__type_chat = 'chat'

    # Extrai todos os números
    def list_phones(self, date: str = None) -> list:
        """
        Função retorna todos os números que enviaram mensagem na conversa
        """

        list_phones = list({item['phone'] for item in self.filter_data(date=date)})

        return list_phones

    # Conta a quantidade de mensagens por numero ou conversa e por data
    def count_messages(self, phone: str = None, date: str = None) -> list:
        """
        Retorna a quantidade de mensagens
        :param date: Recebe Data para filtragem
        :type date: string
        :param phone: Recebe o número que deve buscar
        :type phone: string
        :return:
        """
        list_return = []
        if phone:
            list_return.append({"phone": phone, "messages_number": len(self.filter_data(phone=phone, date=date))})
        else:
            [list_return.append({'phone': number, 'messages_number': len(self.filter_data(phone=number, date=date))})
             for number in self.list_phones(date=date)]

        return sorted(list_return, key=lambda k: k['messages_number'], reverse=True)

    # Pode extrair links de conversar ou numero e por data
    def extract_links(self, phone: str = None, date: str = None) -> list:
        list_message = []

        midia_file = 0

        # Adiciona todas as mensagens em uma lista
        for item in self.filter_data(phone=phone, date=date):
            if item['message'].replace(' ', '') != '<arquivodemídiaoculto>':
                list_message.append(item['message'])
            else:
                # captura a quantidade de arquivos de midia enviado
                midia_file += 1

        # Cria uma lista com todas as palavras separadas por espaço
        str_message = ' '.join(list_message)

        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
                r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])) "
        url = re.findall(regex, str_message)

        return [x[0] for x in url]

    def word_occurrence_counter(self, phone: str, remove_punctuation: bool = False) -> dict:
        """
        Retorna uma lista de ocorrencias de todas as palavras enviadas pelo número especificado
        """
        list_message, midia_file = [], 0

        # Adiciona todas as mensagens em uma lista
        for item in self.filter_data(phone=phone):
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

    def word_cloud(self, phone: str = None, date: str = None) -> None:
        list_message, midia_file = [], 0

        # Adiciona todas as mensagens em uma lista
        for item in self.filter_data(phone=phone, date=date):
            if item['message'].replace(' ', '') != '<arquivodemídiaoculto>':
                if item['message'].replace(' ', '') != 'mensagemapagada':
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
        plt.savefig(self.__folder_word_cloud + phone.replace(" ", "") if phone is not None else 'Grupo')


if __name__ == '__main__':
    # classe = SearchInExportChat("conversa")
    numero = 'Paulo Mota'

    # print(classe.extract_list_phones())

    # print(classe.filter_data(phone=numero))

    # print(classe.filter_data(phone=numero, message='demorando', date='2022-01-16T00:00:00.00'))

    # print(classe.word_cloud(date='2022-01-09T00:00:00.00'))

    # print(classe.extract_links())

    # print(classe.count_messages(phone='+55 21 97027-6712'))
    # print(classe.count_messages())
    classe = SearchInExportChat("conversa")
    # Quantidade de mensagens enviada por cada participante
    [print(_) for _ in classe.count_messages()]

    # Colocar links para o telefone e ter uma tela com as estatisticas dele
    # desistalar o pandas
