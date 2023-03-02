import os

from dotenv import load_dotenv
from sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

connection_string = URL.create(
    drivername=os.getenv('DB_DRIVERNAME'),
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    port=os.getenv('DB_PORT'),
)

# Declarando bases e tabelas
Base = declarative_base()
from src.models.entities import *

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
