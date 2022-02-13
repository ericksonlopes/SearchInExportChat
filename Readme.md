/uploader
Carrega o arquivo na api

/filter
````json
{
    "phone": "Paulo Mota",
    "date": "2022-01-16T00:00:00.00",
    "message": "celular"
}
````
Resulta:
````json
[
    {
        "date": "Sun, 26 Dec 2021 13:46:00 GMT",
        "message": "obrigado",
        "phone": "+55 31 8950-6741"
    },
    {
        "date": "Sun, 26 Dec 2021 17:16:00 GMT",
        "message": "preço da gazoza aqui",
        "phone": "Paulo Mota"
    }
]
````

/list-numbers
```json
[
    "+55 11 90000-0000",
    "+55 11 90000-0000",
    "+55 11 70000-0000",
    "+55 11 90000-0000",
    "+55 11 90000-0000"
]
```

/list-links
````json
{
    "phone": null
}
````

/word-occurence
```json
{
    "phone": null,
    "punctuation": null
}
```

/word-cloud
```text
Retorna uma imagem
```