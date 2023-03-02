from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer

from config.sqlalchemy_config import Base


class FilesTable(Base):
    __tablename__ = 'files'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(255))
    path = Column('path', String(255))
    created_at = Column('created_at', DateTime, default=datetime.now())

    def __repr__(self):
        return f'File - {self.id} - {self.name}'
