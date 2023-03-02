# Instalação 🛠️

[![Python package](https://github.com/Erickson-lopes-dev/SearchInExportChat/actions/workflows/python-app.yml/badge.svg)](https://github.com/Erickson-lopes-dev/SearchInExportChat/actions/workflows/python-app.yml)

[![Supported Python Versions](https://img.shields.io/pypi/pyversions/rich/10.11.0)](https://www.python.org/download/) ![Pytest](https://img.shields.io/badge/-Pytest-0A9EDC?&logo=Pytest&logoColor=FFFFFF)  ![Pandas](https://img.shields.io/badge/-pandas-150458?&logo=pandas&logoColor=FFFFFF)

```python
git
clone
https: // github.com / Erickson - lopes - dev / SearchInExportChat - API
cd
SearchInExportChat - API /
```

Crie uma máquina virtual para rodar o projeto.

```python
python3 - m
venv
venv
```

Uma vez criado o seu ambiente virtual, deve ativá-lo.

No Unix ou no MacOS, executa:

```
source venv/bin/activate
```

No Windows, execute:

```python
call
venv\Scripts\activate.bat
```

Com o ambiente virtual ativado, instale as dependências (certifique-se de que esteja na mesma pasta que o arquivo).

```python
pip
install - r
requirements.txt
```

# Como Utilizar a classe

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
# Lista os numeros que são encontrado na datas determinada
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
# Conta quantidadede de mensagens que o número passado
print(classe.get_message_count_by_phone())
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
print(classe.get_message_count_by_phone())

# Conta quantas mensagens todos os numeros enviaram
print(classe.get_message_count_by_phone())
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

![img](https://user-images.githubusercontent.com/62525983/154390872-19003660-386e-47d6-aef7-83f6d29a6660.png)

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


