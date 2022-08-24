from src.searc_in_export_chat import SearchInExportChat

classe = SearchInExportChat("conversa.txt")
numero = 'Paulo Mota'

# Filtragem com todos os parametros
# print(classe.filter_data(phone=numero, message='demorando', date='2022-01-16T00:00:00.00'))

# Traz todos os dados
# all_data = classe.filter_data(phone=numero)
# [print(item.__dict__) for item in all_data]

# # Conta quantidadede de mensagens que o numero passado
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
print(classe.word_cloud(phone="Paulo Mota", date='2022-01-09T00:00:00.00'))

# Conta quantas vezes o numero determinado digitou especificas palavras
# print(classe.word_occurrence_counter(phone='Paulo Mota'))
