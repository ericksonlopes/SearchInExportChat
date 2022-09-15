from datetime import datetime

from src.filters import FilterDataHandle

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

# # Lista os numeros que são encontrado na data determinada
# print(classe.list_phones(date='2022-01-16T00:00:00.00'))
# # Lista todos os numeros encontrado na conversa
# print(classe.list_phones())

# Gera o word cloud
# print(classe.word_cloud(phone="Paulo Mota", date='2022-01-09T00:00:00.00'))

# Conta quantas vezes o numero determinado digitou especificas palavras
# print(classe.word_occurrence_counter(phone='Paulo Mota'))

if __name__ == '__main__':
    from src.models import FilterMessagesModel, MessageDto

    # data = FilterDataHandle('tests/test_file_folder/test_group.txt')
    #
    # start_date = datetime(2022, 6, 22)
    # end_date = datetime(2022, 6, 23)
    # filter_message = FilterMessagesModel(
    #     phone='@erickson',
    #     message='olá', start_date=start_date,
    #     end_date=end_date)
    #
    # print(filter_message(data.messages))

    data = FilterDataHandle('file_folder/conversa.txt')
    # data = FilterDataHandle('tests/test_file_folder/test_group.txt')
    print([item.phone for item in data.extract_links()])
    print(data.extract_links())

    # start_date = datetime(2022, 6, 22)
    # end_date = datetime(2022, 6, 23)

    # filter_message = FilterMessagesModel(
    #     phone='@erickson',
    #     message='olá',
    #     start_date=start_date,
    #     end_date=end_date)

    # print(filter_message(data.messages))
    # print(data.count_messages())

    # print(data.get_list_of_numbers())

    # dto = MessageDto(list_phone=['@erickson.lds', 'Paulo Mota'])

    # for item in data.count_messages():
    #     print(f'{item.phone:>20}: {item.quantity}')


