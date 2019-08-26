import os
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine(f'sqlite:///{os.path.dirname(os.path.abspath(__file__))}/sqlite.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)