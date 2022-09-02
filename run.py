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
    data = FilterDataHandle('tests/test_file_folder/test_group.txt')

    start_date = datetime(2022, 6, 22)
    end_date = datetime(2022, 6, 23)
    print(data.get_list_of_numbers(start_date, end_date))
    # info_messages = data.info_messages

    # df_messages = pd.DataFrame(data.messages)
    #
    # print(df_messages['phone'].value_counts().head(10))

    # primeira e ultima mensagem
    # print(min(df_messages.date.values))
    # print(max(df_messages.date.values))
    # print(df_messages.value_counts('phone'))
