import sqlite3
import os


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
