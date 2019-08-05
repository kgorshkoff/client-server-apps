import yaml
import json
import datetime
import hashlib
import logging
from socket import socket
from datetime import datetime
from argparse import ArgumentParser


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
args = parser.parse_args()

default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


logging.debug(f'Client started with next settings {default_config}')

host, port = default_config.get('host'), default_config.get('port')
sock = socket()
sock.connect((host, port))

logging.info(f'Client started and connected to {host}:{port}')

action = input('Enter action: ')
data = input('Enter data: ')

hash_obj = hashlib.sha256()
hash_obj.update(
    str(datetime.now().timestamp()).encode()
)

request = {
    'action': action,
    'time': datetime.now().timestamp(),
    'data': data,
    'token': hash_obj.hexdigest()
}

s_request = json.dumps(request)

sock.send(s_request.encode())
logging.debug(f'Client sent data: {s_request}')
b_response = sock.recv(default_config.get('buffersize'))
response = b_response.decode()
logging.debug(f'Client recieved response: {response}')
print(response)
logging.info('Client closed')