import yaml
import json
import responses
from socket import socket
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

host, port = default_config.get('host'), default_config.get('port')

try:
    sock = socket()
    sock.bind((host, port))
    sock.listen(5)

    print(f'Server is running {host}:{port}')

    while True:
        client, address = sock.accept()
        print(f'Client connected: {address[0]}:{address[1]}')
        
        b_request = client.recv(default_config.get('buffersize'))
        request = json.loads(b_request.decode())
        response = responses.form_response(request)

        client.send(response)
        client.close()

except KeyboardInterrupt:
    print('Server shutting down')