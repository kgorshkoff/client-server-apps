import os
from sqlalchemy import create_engine, Table, String, Integer, DateTime, Column, MetaData
from sqlalchemy.orm import mapper

engine = create_engine(f'sqlite:///{os.path.dirname(os.path.abspath(__file__))}/sqlite.db')
metadata = MetaData()

responses = Table(
    'responses', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('action', String),
    Column('datetime', DateTime),
    Column('data', String),
    Column('code', Integer)
)

metadata.create_all(engine)

class Response:
    def __init__(self, username, action, datetime, data, code):
        self.username = username
        self.action = action
        self.datetime = datetime
        self.data = data
        self.code = code


mapper(Response, responses)