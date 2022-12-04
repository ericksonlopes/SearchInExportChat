from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey

from sqlalchemy_config import Base


class InfoMessagesTable(Base):
    __tablename__ = 'info_messages'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    id_file = Column('id_file', Integer, ForeignKey('files.id'), nullable=False)
    message = Column('message', String)
    date = Column('date', DateTime)
    created_at = Column('created_at', DateTime, default=datetime.now())
