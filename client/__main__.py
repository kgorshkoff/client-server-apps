import sys
import os
import yaml
import json
import logging
from datetime import datetime
from argparse import ArgumentParser
from app import Application


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
    required=False, help='set client buffersize'
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
            os.path.dirname(os.path.abspath(__file__)) + '/logs/' + datetime.today().strftime("%Y%m%d") + '_client_main.log')
    ]
)


# with Application(args) as client:
#     client.connect()
#     client.run()
