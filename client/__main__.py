import yaml
import json
import datetime
from logs import log
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

log.logger.debug(f'Client started with next settings {default_config}')

host, port = default_config.get('host'), default_config.get('port')
sock = socket()
sock.connect((host, port))

log.logger.info(f'Client started and connected to {host}:{port}')

action = input('Enter action: ')
data = input('Enter data: ')

request = {
    'action': action,
    'time': datetime.now().timestamp(),
    'data': data
}

s_request = json.dumps(request)

sock.send(s_request.encode())
log.logger.debug(f'Client sent data: {s_request}')
b_response = sock.recv(default_config.get('buffersize'))
response = b_response.decode()
log.logger.debug(f'Client recieved response: {response}')
print(response)
log.logger.info('Client closed')