import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Pasta atual
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# string de conexão com o banco
connection_string = "sqlite:///" + os.path.join(BASE_DIR, 'data_wpp.db')

# Declarando bases e colunas
Base = declarative_base()
from src.models.tables import *

# Criando engine com o banco de conexão
engine = create_engine(connection_string, echo=False)

# criação da sessão
Session = sessionmaker()


class Conector:
    def __init__(self):
        self.session = Session(bind=engine)

    def __enter__(self):
        return self.session

    def __exit__(self, *args, **kwargs):
        self.session.commit()
        self.session.close()
