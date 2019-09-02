from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String

from database import Base


class Response(Base):
    __tablename__ = 'responses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.now())
    username = Column(String)
