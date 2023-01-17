from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey

from sqlalchemy_config import Base


class MessagesTable(Base):
    __tablename__ = 'messages'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    id_file = Column('id_file', Integer, ForeignKey('files.id'), nullable=False)
    phone = Column('phone', String(32))
    message = Column('message', String)
    date = Column('date', DateTime)
    created_at = Column('created_at', DateTime, default=datetime.now())