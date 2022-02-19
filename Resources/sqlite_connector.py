from Resources.searc_in_export_chat import DataFileCleaner
from typing import List
import sqlite3
import os


class ActionsSQlite:
    def __init__(self):
        self.__file = os.getenv('FILE_DB')

        if not os.path.isfile(self.__file):
            conn = sqlite3.connect(self.__file)
            # Cria a tabela files
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uuid TEXT NOT NULL,
                    path_name TEXT NOT NULL,
                    name_file TEXT NOT NULL ,
                    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,     
                    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )""")
            # Cria a tabela messages
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT NOT NULL,
                    date DATETIME NOT NULL,
                    message TEXT NOT NULL,
                    file_id INTEGER NOT NULL,
                    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,    
                    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
                    FOREIGN KEY (file_id) REFERENCES files(id)
                    )
                    """)

            conn.close()

    @classmethod
    def load_data(cls, id_uuid: str, path: str, file: str):
        with SQLiteCursor() as cursor:
            # Insere os dados do nvoo arquivo
            sql = "insert into files (uuid, path_name, name_file) values (?, ?, ?)"
            datas = (id_uuid, path, file)
            cursor.execute(sql, datas)

        with SQLiteCursor() as cursor:
            # busca o id do novo arquivo criado
            sql = "select id, uuid from files where uuid=?"
            id_new_file = cursor.execute(sql, [id_uuid]).fetchall()

        id_file = id_new_file[0][0]
        id_uuid = id_new_file[0][1]

        messages = DataFileCleaner().clear_data(file=id_uuid, id_file=id_file)

        with SQLiteCursor() as cursor:
            sql = "insert into messages (file_id, phone, date, message) values (?, ?, ?, ?)"
            cursor.executemany(sql, messages)


class SQLiteCursor(ActionsSQlite):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(os.getenv('FILE_DB'))

    def __enter__(self):
        return self.conn.cursor()

    def __exit__(self, error: Exception, value: object, traceback: object):
        self.conn.commit()
        self.conn.close()


class SelectBuilder:
    def __init__(self, fields=None):
        if fields is None or fields[0] == '':
            fields = ['*']

        self.__fields = fields
        self.__table_name = ''
        self.__conditions = []
        self.__sort_field = ''

    def from_(self, table_name: str):
        self.__table_name = table_name
        return self

    def where(self, conditions: List):
        self.__conditions = conditions
        return self

    def order_by(self, field: str):
        self.__sort_field = field
        return self

    def __str__(self):
        return 'SELECT {} FROM {}{}{}'.format(
            ', '.join(self.__fields),
            self.__table_name,
            ' WHERE {}'.format(' AND '.join(self.__conditions)) if self.__conditions else '',
            ' ORDER BY {}'.format(self.__sort_field) if self.__sort_field else ''
        )
