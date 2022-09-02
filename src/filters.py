from datetime import datetime
from typing import List

from src.clear_file import ClearDataFiles


class FilterDataHandle(ClearDataFiles):
    def __init__(self, pathfile: str):
        super().__init__(pathfile)

    def get_list_of_numbers(self, start_date: datetime = None, end_date: datetime = None) -> List[str]:
        """Get list of numbers"""
        if start_date and end_date:
            return list(set([message.phone for message in self.messages if start_date <= message.date <= end_date]))

        return list({item.phone for item in self.messages})

# import os
# import re
# import string
# import uuid
# from collections import Counter
# from typing import List
#
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
#
# from src.clear_file import ClearDataFiles
# from src.helpers.stop_words import stopwordsnltk
# from src.models import NumberOfMessagesModel, WordQuantityModel
#
#
# class SearchInExportChat(ClearDataFiles):
#     def __init__(self, file: str):
#         super().__init__(file)
#         self.__type_chat: str
#
#         # Verifica se é uma conversa ou grupo
#         if len(self.list_phones()) > 2:
#             self.__type_chat = 'grupo'
#         else:
#             self.__type_chat = 'chat'
#
#     def list_phones(self, date: str = None) -> list:
#         """
#         Função retorna todos os números que enviaram mensagem na conversa
#         """
#
#         list_phones = list({item.phone for item in self.filter_data(date=date)})
#
#         return list_phones
#
#     def count_messages(self, phone: str = None, date: str = None) -> List[NumberOfMessagesModel]:
#         """
#         Retorna a quantidade de mensagens enviadas por um número
#         :param date: Recebe Data para filtragem
#         :type date: string
#         :param phone: Recebe o número que deve buscar
#         :type phone: string
#         :return:
#         """
#         list_return = []
#         if phone:
#             list_return.append(NumberOfMessagesModel(phone, len(self.filter_data(phone=phone, date=date))))
#
#         else:
#             [list_return.append(NumberOfMessagesModel(number, len(self.filter_data(phone=phone, date=date))))
#              for number in self.list_phones(date=date)]
#
#         return sorted(list_return, key=lambda k: k.amount, reverse=True)
#
#     def extract_links(self, phone: str = None, date: str = None) -> List[str]:
#         """
#         Extrai todas as links
#
#         :param phone: str
#         :param date: str
#         :return:
#         """
#         str_message = ' '.join([_.message for _ in self.filter_data(phone=phone, date=date)])
#
#         regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
#                 r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
#
#         url = re.findall(regex, str_message)
#
#         return [x[0] for x in url]
#
#     def word_occurrence_counter(self, phone: str = None, remove_punctuation: bool = False, date: str = None):
#         """
#         Retorna uma lista de ocorrencias de todas as palavras enviadas pelo número especificado
#         """
#         list_message, midia_file = [], 0
#
#         # Adiciona todas as mensagens em uma lista
#         for item in self.filter_data(phone=phone, date=date):
#             if item.message.replace(' ', '') != '<arquivodemídiaoculto>':
#                 list_message.append(item.message)
#             else:
#                 # captura a quantidade de arquivos de midia enviado
#                 midia_file += 1
#
#         # Cria uma lista com todas as palavras separadas por espaço
#         str_message = ' '.join(list_message)
#
#         # Remove a pontuação
#         if remove_punctuation:
#             for item in string.punctuation:
#                 str_message = str_message.replace(item, '')
#
#         # Separa a string por espaços para formar uma lista
#         str_message = str_message.split()
#
#         # retira as stopwords
#         str_message = [item for item in str_message if item not in stopwordsnltk]
#
#         # Realiza a da lista contagem com o pandas
#         str_dict = dict(Counter(str_message))
#
#         # Junta o dicionario com outro(s)
#         str_dict = {**{"Arquivos de midia": midia_file}, **str_dict}
#
#         # ordena a lista
#         ordered = sorted(str_dict.items(), key=lambda x: x[1], reverse=True)
#
#         # Transforma a lista de tupla em dicionario
#         return_ordered = [WordQuantityModel(word=x, amount=y) for x, y in
#                           zip([_[0] for _ in ordered], [_[1] for _ in ordered])]
#
#         return return_ordered
#
#     def word_cloud(self, phone: str = None, date: str = None) -> str:
#         """
#         Gera uma imagem word_cloud
#         :param phone:
#         :param date:
#         :return:
#         """
#         folder_word_cloud = 'word_cloud/'
#
#         if not os.path.exists(folder_word_cloud):
#             os.mkdir(folder_word_cloud)
#
#         list_message, midia_file = [], 0
#
#         # Adiciona todas as mensagens em uma lista
#         for item in self.filter_data(phone=phone, date=date):
#             if item.message.replace(' ', '') != '<arquivodemídiaoculto>':
#                 if item.message.replace(' ', '') != 'mensagemapagada':
#                     list_message.append(item.message)
#             else:
#                 # captura a quantidade de arquivos de midia enviado
#                 midia_file += 1
#
#         # Cria uma lista com todas as palavras separadas por espaço
#         str_message = ' '.join(list_message)
#
#         # Separa a string por espaços para formar uma lista
#         str_message = str_message.split()
#
#         # retira as stopwords
#         str_message = [item for item in str_message if item not in stopwordsnltk]
#
#         # Rega o word cloud
#         wordcloud = WordCloud().generate(' '.join(str_message))
#
#         # Cria um img
#         plt.axis('off')
#         plt.imshow(wordcloud, interpolation="bilinear")
#
#         arquivo = f"{folder_word_cloud}{phone.replace(' ', '') if phone is not None else 'Grupo'}" \
#                   f"{str(uuid.uuid1())}.png"
#
#         # Salva a imagem
#         plt.savefig(arquivo)
#
#         # Retorna o arquivo
#         return arquivo
