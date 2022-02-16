import sqlite3
import os

from searc_in_export_chat import ClearDataFiles


class ConnectDB:
    def __init__(self):
        self.__file = 'wpp-search.db'

        if not os.path.isfile(self.__file):
            conn = sqlite3.connect(self.__file)

            conn.execute("""
                    CREATE TABLE files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uuid TEXT NOT NULL,
                    path_name TEXT NOT NULL,
                    name_file TEXT NOT NULL ,
                    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,     
                    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )""")

            conn.execute("""
                    CREATE TABLE messages (
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

    def connect(self):
        return sqlite3.connect(self.__file)


class AddDataToDB(ConnectDB):
    def __init__(self):
        super().__init__()

    def init_add_file(self, id_uuid: str, path: str, file: str):
        connect = self.connect()
        cursor = connect.cursor()

        # Insere os dados do nvoo arquivo
        sql = "insert into files (uuid, path_name, name_file) values (?, ?, ?)"
        datas = (id_uuid, path, file)
        cursor.execute(sql, datas)

        # busca o id do novo arquivo criado
        sql = "select id, uuid from files where uuid=?"
        id_new_file = cursor.execute(sql, [id_uuid]).fetchall()

        connect.commit()
        cursor.close()
        print(id_new_file)
        # retorna o novo id
        self.__add_data(id_file=id_new_file[0][0], id_uuid=id_new_file[0][1])

    def __add_data(self, id_file: int, id_uuid: str):
        data = ClearDataFiles().clear_data(file=id_uuid, id_file=id_file)
        connect = self.connect()
        cursor = connect.cursor()

        sql = "insert into messages (file_id, phone, date, message) values (?, ?, ?, ?)"

        cursor.executemany(sql, data)

        connect.commit()
        cursor.close()


class FiltersDB(ConnectDB):
    def __init__(self):
        super().__init__()
