from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
# from auth.models import User


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='messages')

#
# class Message(Base):
#     __tablename__ = 'message'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     data = Column(String, nullable=True)
#     created = Column(DateTime, default=datetime.now())
#     user_id = Column(Integer, ForeignKey('users.id'))
#     user = relationship('User', back_populates='messages')
#
