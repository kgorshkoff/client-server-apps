import os
import json
import threading
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


def read(sock, connections, requests, buffersize):
    try:
        b_request = sock.recv(buffersize)
    except Exception:
        connections.remove(sock)
    else:
        if b_request:
            requests.append(b_request)


def write(sock, connections, response):
    try:
        sock.send(response)
    except Exception:
        connections.remove(sock)



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
        logging.FileHandler(
            os.getcwd() + '/logs/' + datetime.today().strftime("%Y%m%d") + '_server_main.log', encoding='utf-8'
            ),
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
            r_thread = threading.Thread(
                target=read, args=(r_client, connections, requests, default_config.get('buffersize'))
                )
            r_thread.start()

        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)

            for w_client in wlist:
                w_thread = threading.Thread(
                target=write, args=(w_client, connections, b_response)
                )
                w_thread.start()


except KeyboardInterrupt:
    logging.info('Server shutting down')
