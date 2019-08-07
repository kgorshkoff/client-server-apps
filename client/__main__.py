import os
import yaml
import json
import datetime
import hashlib
import logging
import threading
import zlib
from socket import socket
from datetime import datetime
from argparse import ArgumentParser


def read(sock, buffersize):
    while True:
        compressed_response = sock.recv(buffersize)
        b_response = zlib.decompress(compressed_response)
        response = b_response.decode()

        logging.debug(f'Client recieved response: {response}')

        if 'messenger' in response:
            json_response = json.loads(response)
            print(f"{datetime.fromtimestamp(json_response.get('time')).strftime('%H:%M:%S')} | {json_response.get('username')}: {json_response.get('data')}")
        else:
            print(response)

parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='sets config file path'
)
# parser.add_argument(
#     '-m', '--mode', type=str, default='r',
#     required=True, help='sets client mode'
# )
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
    'buffersize': 1024,
    'mode': 'r'
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getcwd() + '/logs/' + datetime.today().strftime("%Y%m%d") + '_client_main.log', encoding='utf-8'),
        # logging.StreamHandler()
    ]
)

logging.debug(f'Client started with next settings {default_config}')

host, port = default_config.get('host'), default_config.get('port')
sock = socket()
sock.connect((host, port))

logging.info(f'Client started and connected to {host}:{port}')
print('Welcome to geek-chat!')

try:
    read_thread = threading.Thread(
        target=read, args=(sock, default_config.get('buffersize'))
        )
    read_thread.start()

    username = input('Enter your name: ')
    
    while True:
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )

        action = input('Enter action: ')
        data = input('Enter data: ')

        request = {
            'username': username,
            'action': action,
            'time': datetime.now().timestamp(),
            'data': data,
            'token': hash_obj.hexdigest()
        }

        s_request = json.dumps(request)
        b_request = zlib.compress(s_request.encode())

        sock.send(b_request)
        logging.debug(f'Client sent data: {data}')
except KeyboardInterrupt:
    sock.close()
    print('Client closed')