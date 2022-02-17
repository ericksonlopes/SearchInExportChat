
## Instancie a classe
```python
sec = SearchInExportChat("conversa")
```

## Filtro padrão
```python
# Filtragem com todos os parametros
filtro = sec.filter_data(phone='+55 00 0000-0000', message='demorando', date='2022-01-16T00:00:00.00')
print(filtro)

# Traz todos os dados 
filtro = sec.filter_data()
```
Saída:
```python
[
    {'phone': 'Paulo Mota', 'date': datetime.datetime(2022, 1, 16, 9, 34), 'message': 'tava demorando'},
    ...
]
```

## Lista todos os contatos
```python
# Lista os numeros que são encontrado na data determinada
print(classe.list_phones(date='2022-01-16T00:00:00.00'))
# Lista todos os numeros encontrado na conversa
print(classe.list_phones())
```
Saída:
```python
[
    '+55 00 0000-0000',
    ...
]
```

## Contador de mensagens
```python
# Conta quantidadede de mensagens que o numero passado
print(classe.count_messages(phone='@erickson.lds'))
```
Saída:
```python
[
    {'phone': '@erickson.lds', 'messages_number': 373},
    ...
]
```

## Contador de mensagens
```python
 # Conta quantidadede de mensagens que o numero passado com todos os filtros
print(classe.count_messages(phone='@erickson.lds', date='2022-01-16T00:00:00.00'))

# Conta quantas mensagens todos os numeros enviaram
print(classe.count_messages())
```
Saída:
```python
[
    {'phone': '+55 00 0000-0000', 'messages_number': 3560},
    ...
]
```


## Extrair links
```python
 # Extrai todos os links dentro dos filtros
print(classe.extract_links(phone='Paulo Mota', date='2022-01-16T00:00:00.00'))
# Extrai todos os links
print(classe.extract_links())
```
Saída:
```python
[
    'https://github.com',
    'https://www.udacity.com',
    ...
]
```

## Imagem com word cloud
```python
classe.word_cloud(date='2022-01-09T00:00:00.00')
```
Saída:
![](word_cloud/Grupo1bf6ea49-8f8c-11ec-b2f5-3c7c3f7809c7.png)



## Conta ocorrencia de palavras
```python
# Conta quantas vezes o numero determinado digitou especificas palavras
print(classe.word_occurrence_counter(phone='@erickson.lds'))
```
Saída:
```python
[
    {'Arquivos de midia': 72}, 
    {'amigo': 51},
    {'Bom': 33},
    {'dia': 33}, 
    ...
]
```