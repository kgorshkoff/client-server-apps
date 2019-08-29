from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from echo.models import Message


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    sessions = relationship('Session', backref='sessions')
    messages = relationship('Message', backref='messages')


class Session(Base):
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, default=datetime.now())
    user_id = Column(ForeignKey('users.id'))
    user = relationship('User', back_populates='users')