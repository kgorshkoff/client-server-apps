import json
from socket import socket
from argparse import ArgumentParser
import yaml
from resolvers import resolve
from protocol import validate_request, make_response
from log import server_log_config as log

import sys
sys.path.append('/Users/kirill/PycharmProjects/client-server-apps/')

print(sys.path)

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

try:
    sock = socket()
    sock.bind((host, port))
    sock.listen(5)

    log.logger.info(f'Server is running {host}:{port}')

    while True:
        client, address = sock.accept()
        log.logger.info(f'Client connected: {address[0]}:{address[1]}')

        b_request = client.recv(default_config.get('buffersize'))
        request = json.loads(b_request.decode())

        if validate_request(request):
            action_name = request.get('action')
            controller = resolve(action_name)
            if controller:
                try:
                    log.logger.debug(f'Controller {action_name} resolved with request: {b_request.decode()}')
                    response = controller(request)
                except Exception as err:
                    log.logger.critical(f'Controller {action_name} error {err}')
                    response = make_response(request, 500, 'Internal server error')
            else:
                log.logger.error(f'Controller {action_name} not found')
                response = make_response(request, 404, f'Action with name {action_name} is not supported')
        else:
            log.logger.error(f'Wrong controller request: {request}')
            response = make_response(request, 400, 'wrong request format')

        client.send(
            json.dumps(response).encode()
        )

        log.logger.info(f'Client disconnected: {address[0]}:{address[1]}')
        client.close()
except KeyboardInterrupt:
    log.logger.info('Server shutting down')