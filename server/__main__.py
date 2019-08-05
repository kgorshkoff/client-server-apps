import os
import json
from datetime import datetime
from socket import socket
from argparse import ArgumentParser
import yaml
import select
from server.resolvers import resolve
from server.handlers import handle_default_request
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
        logging.FileHandler(os.getcwd() + '/logs/' + datetime.today().strftime("%Y%m%d") + '_server_main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

requests = []
connections = []

try:
    sock = socket()
    sock.bind((host, port))
    sock.settimeout(0)
    sock.listen(5)

    logging.info(f'Server is running {host}:{port}')

    while True:
        try:
            client, address = sock.accept()
            connections.append(client)
            logging.info(f'Client connected: {address[0]}:{address[1]} | connections: {len(connections)}')
        except:
            pass

        rlist, wlist, xlist = select.select(
            connections, connections,  connections, 0
        )

        for r_client in rlist:
            b_request = r_client.recv(default_config.get('buffersize'))
            requests.append(b_request)

        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)

            for w_client in wlist:
                w_client.send(b_response)


except KeyboardInterrupt:
    logging.info('Server shutting down')
