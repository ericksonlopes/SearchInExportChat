from datetime import datetime

from src.add_messages import AddMessages
from src.filters import FilterDataHandleBase

# classe = SearchInExportChat("test_group.txt")
# numero = '@erickson.lds'

# Filtragem com todos os parametros
# print(classe.filter_data(phone=numero, message='demorando', date='2022-01-16T00:00:00.00'))

# Traz todos os dados
# all_data = classe.filter_data(phone=numero)
# [print(item.__dict__) for item in all_data]

# # Conta quantidadede de mensagens que o numero passado
# print(classe.filter_data(phone=numero))
# print(classe.count_messages(phone='@erickson.lds'))
# Conta quantas mensagens todos os numeros enviaram
# print(classe.count_messages())

# # Extrai todos os links dentro dos filtros
# print(classe.extract_links(phone='Paulo Mota', date='2022-01-16T00:00:00.00'))
# # Extrai todos os links
# print(classe.extract_links())

# # Lista os numeros que são encontrado na datas determinada
# print(classe.list_phones(date='2022-01-16T00:00:00.00'))
# # Lista todos os numeros encontrado na conversa
# print(classe.list_phones())

# Gera o word cloud
# print(classe.word_cloud(phone="Paulo Mota", date='2022-01-09T00:00:00.00'))

# Conta quantas vezes o numero determinado digitou especificas palavras
# print(classe.word_occurrence_counter(phone='Paulo Mota'))

if __name__ == '__main__':
    AddMessages(pathfile='file_folder/conversa.txt')

    # from src.models import FilterMessagesModel, MessageDto
    #
    # datas = FilterDataHandle('file_folder/conversa.txt')
    #
    # start_date = datetime(2022, 6, 22)
    # end_date = datetime(2022, 6, 23)
    #
    # filter_message = FilterMessagesModel()
    #
    # for item in datas.messages:
    #     print(item, end='\n')

    # print(filter_message(datas.messages))

    # data = FilterDataHandle('file_folder/conversa.txt')
    # # datas = FilterDataHandle('tests/test_file_folder/test_group.txt')
    # # print([item.phone for item in data.extract_links()])
    #
    # message = MessageDto(phone='@erickson.lds')
    #
    # print(data.extract_links(MessageDto()))

    # start_date = datetime(2022, 6, 22)
    # end_date = datetime(2022, 6, 23)

    # filter_message = FilterMessagesModel(
    #     phone='@erickson',
    #     message='olá',
    #     start_date=start_date,
    #     end_date=end_date)

    # print(filter_message(datas.messages))
    # print(datas.count_messages())

    # print(datas.get_list_of_numbers())

    # dtos = MessageDto(list_phone=['@erickson.lds', 'Paulo Mota'])

    # for item in datas.count_messages():
    #     print(f'{item.phone:>20}: {item.quantity}')


