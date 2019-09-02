import os
import yaml
import logging
from datetime import datetime
from argparse import ArgumentParser
from app import Server
from handlers import handle_default_request
from database import engine, Base
from settings import INSTALLED_MODULES, BASE_DIR


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
parser.add_argument(
    '-m', '--migrate', action='store_true',
    required=False, help='migrates database'
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
            BASE_DIR + '/logs/' + datetime.today().strftime("%Y%m%d") + '_server_main.log'),
        logging.StreamHandler()
            ]
    )   


if args.migrate:
    module_name_list = [f'{item}.models' for item in INSTALLED_MODULES]
    module_path_list = (os.path.join(BASE_DIR, item, 'models.py') for item in INSTALLED_MODULES)
    for index, path in enumerate(module_path_list):
        if os.path.exists(path):
            __import__(module_name_list[index])
    Base.metadata.create_all(engine)
else:
    app = Server(
        args=args, 
        handler=handle_default_request
        )

    app.bind()
    app.run()
