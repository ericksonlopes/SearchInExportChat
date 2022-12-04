import re
from collections import Counter
from datetime import datetime
from typing import List

from loguru import logger

from config import setup_logger
from src.clear_file import ClearDataFile
from src.models import MessageDto, FilterMessagesModel, NumberOfMessagesModel, PhoneLinksModel


class FilterDataHandle(ClearDataFile):

    def __init__(self, pathfile: str):
        super().__init__(pathfile)
        setup_logger()

    @property
    def group_or_privaty(self) -> str:
        """Return group or private"""
        try:
            len_phones = len(self.get_list_of_numbers())
        except Exception as error:
            logger.error(error)
            raise error

        result: str
        if len_phones > 2:
            result = 'group'

        elif len_phones == 2:
            result = 'private'
        else:
            result = 'unknown'

        logger.info(f'{self.path_file} is {result}')

        return result

    def get_list_of_numbers(self, start_date: datetime = None, end_date: datetime = None) -> List[str]:
        """Get list of numbers"""
        try:
            filtro_message = FilterMessagesModel(start_date=start_date, end_date=end_date)
            messages = filtro_message(self.messages)

        except Exception as error:
            logger.error(error)
            raise error

        logger.info(f'Successfully extracted {len(messages)} messages')
        return list({message.phone for message in messages})

    def get_message_count_by_phone(self, message_dto: MessageDto = MessageDto()) -> List[NumberOfMessagesModel]:
        """Count messages"""

        try:
            # create filter
            filter_message = FilterMessagesModel(**message_dto())

            # filter messages
            messages_filter = filter_message(self.messages)

            # Perform message count
            messages = Counter(message.phone for message in messages_filter)

            # Arrange in ascending order
            messages_sorted = sorted(messages.items(), key=lambda message: message[1], reverse=True)

            # Return list of objects
            list_count = list(map(lambda _: NumberOfMessagesModel(phone=_[0], quantity=_[1]), messages_sorted))
        except Exception as error:
            logger.error(error)
            raise error

        logger.info(f'Successfully counted {len(list_count)} messages')
        return list_count

    def extract_links(self, message_dto: MessageDto = MessageDto()) -> List[PhoneLinksModel]:
        """Extract links from messages"""
        try:
            filter_message = FilterMessagesModel(**message_dto())
            messages = filter_message(self.messages)

            list_phone_link: List[PhoneLinksModel] = []

            for message in messages:
                links = re.findall(r'(https?://\S+)', message.message)

                if links:
                    for lista_phone in list_phone_link:
                        if lista_phone.phone == message.phone:
                            [lista_phone.links.append(x) for x in links]
                            break
                    else:
                        list_phone_link.append(PhoneLinksModel(phone=message.phone, links=links))
        except Exception as error:
            logger.error(error)
            raise error

        logger.info(f'Successfully  {len(list_phone_link)}')
        return list_phone_link

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
