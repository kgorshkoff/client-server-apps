import os
import yaml
import logging
from sqlalchemy import create_engine, Table, String, Integer, Column, MetaData
from sqlalchemy.orm import mapper
from datetime import datetime
from argparse import ArgumentParser
from server.app import Server
from server.handlers import handle_default_request


parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='sets config file path'
)
parser.add_argument(
    '-host', '--host', type=str,
    required=False, help='set server IP'
)
parser.add_argument(
    '-p', '--port', type=str,
    required=False, help='set server port'
)
parser.add_argument(
    '-b', '--buffersize', type=str,
    required=False, help='set server buffersize'
)
args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        for k, v in file_config.items():
            args.__setattr__(k, v)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            os.getcwd() + '/logs/' + datetime.today().strftime("%Y%m%d") + '_server_main.log'), 
        logging.StreamHandler()
            ]
    )   


if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/sqlite.db'):
    engine = create_engine(f'sqlite:///{os.path.dirname(os.path.abspath(__file__))}/sqlite.db')
    metadata = MetaData()
    metadata.create_all(engine)


app = Server(
    args=args, 
    handler=handle_default_request
    )

app.bind()
app.run()
