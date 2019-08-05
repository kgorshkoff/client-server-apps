import os
import json
from socket import socket
from argparse import ArgumentParser
import yaml
from server.resolvers import resolve
from server.protocol import validate_request, make_response
import logging
# from server.logs import log


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

host, port = default_config.get('host'), default_config.get('port')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

try:
    sock = socket()
    sock.bind((host, port))
    sock.listen(5)

    logging.info(f'Server is running {host}:{port}')

    while True:
        client, address = sock.accept()
        logging.info(f'Client connected: {address[0]}:{address[1]}')

        b_request = client.recv(default_config.get('buffersize'))
        request = json.loads(b_request.decode())

        if validate_request(request):
            action_name = request.get('action')
            controller = resolve(action_name)
            if controller:
                try:
                    logging.debug(f'Controller {action_name} resolved with request: {b_request.decode()}')
                    response = controller(request)
                except Exception as err:
                    logging.critical(f'Controller {action_name} error {err}')
                    response = make_response(request, 500, 'Internal server error')
            else:
                logging.error(f'Controller {action_name} not found')
                response = make_response(request, 404, f'Action with name {action_name} is not supported')
        else:
            logging.error(f'Wrong controller request: {request}')
            response = make_response(request, 400, 'wrong request format')

        client.send(
            json.dumps(response).encode()
        )

        logging.info(f'Client disconnected: {address[0]}:{address[1]}')
        client.close()
except KeyboardInterrupt:
    logging.info('Server shutting down')
