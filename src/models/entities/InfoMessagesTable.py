from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, Text

from config.sqlalchemy_config import Base


class InfoMessagesTable(Base):
    __tablename__ = 'info_messages'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    id_file = Column('id_file', Integer, ForeignKey('files.id'), nullable=False)
    message = Column('message', Text)
    date = Column('date', DateTime)
    created_at = Column('created_at', DateTime, default=datetime.now())

    def __repr__(self):
        return f'InfoMessage - {self.id} - {self.message}'
