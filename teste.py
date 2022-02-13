# from collections import Counter
#
# counter = Counter(['red', 'red', 'blue'])
#
# print(dict(counter))

# from datetime import datetime
#
# print(datetime(2022, 1, 16, 9, 34))

# x = [('Arquivos de midia', 17), ('cara', 8), ('555198131100', 8), ('mano', 8), ('10', 8), ('grupo', 7), ('gay', 7),
#      ('pq', 7), ('q', 7), ('tipo', 6), ('vcs', 6)]
# print(zip([_[0] for _ in x], [_[1] for _ in x]))
# dict_from_list = dict(zip([_[0] for _ in x], [_[1] for _ in x]))
# print(dict_from_list)
# print(dict(x))

# """
# Tabela mensagem
#
# phone/ data/ mensagem/ grupo-conversa/ uuid-arquivo/
# """

import sqlite3


class ConnectDB:
    def __init__(self):
        conn = sqlite3.connect('wpp-search.db')

        conn.execute("""
        CREATE TABLE files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path_name TEXT,
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


if __name__ == '__main__':
    db = ConnectDB()
