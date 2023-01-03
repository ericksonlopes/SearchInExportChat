from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer

from sqlalchemy_config import Base


class FilesTable(Base):
    __tablename__ = 'files'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String)
    path = Column('path', String)
    # type = Column('type', String(10), nullable=True)
    created_at = Column('created_at', DateTime, default=datetime.now())
