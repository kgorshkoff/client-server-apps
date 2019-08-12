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


class TypedProperty:
    def __init__(self, name, type_name, default=None):
        self.name = "_" + name
        self.type = type_name
        self.default = default if default else type_name()

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError("Значение должно быть типа %s" % self.type)
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Невозможно удалить атрибут")


class Client:
    def __init__(self):
        self.host = TypedProperty('host', str, args.host if args.host else 'localhost')
        self.port = TypedProperty('port', int, args.port if args.port else 8000)
        self.buffersize = TypedProperty('buffersize', int, args.buffersize if args.buffersize else 1024)
        self.log_path = TypedProperty('log_path', str, os.getcwd() + '/logs/' + datetime.today().strftime("%Y%m%d") + '_client_main.log')
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler(self.log_path.default)]
        )

    def run(self):
        self.username = input('Enter your name: ')   
        self.sock = socket()
        self.sock.connect((self.host.default, self.port.default))
        
    def read(self):
        while True:
            compressed_response = self.sock.recv(self.buffersize.default)
            b_response = zlib.decompress(compressed_response)
            response = b_response.decode()

            logging.debug(f'Client recieved response: {response}')

            if 'messenger' in response:
                json_response = json.loads(response)
                print(
                    f"{datetime.fromtimestamp(json_response.get('time')).strftime('%H:%M:%S')} | \
                        {json_response.get('username')}: {json_response.get('data')}"
                    )
            else:
                print(response)
                
    def write(self):
        while True:
            hash_obj = hashlib.sha256()
            hash_obj.update(
                str(datetime.now().timestamp()).encode()
            )
    
            action = input('Enter action: ')
            data = input('Enter data: ')
    
            request = {
                'username': self.username,
                'action': action,
                'time': datetime.now().timestamp(),
                'data': data,
                'token': hash_obj.hexdigest()
            }
    
            s_request = json.dumps(request)
            b_request = zlib.compress(s_request.encode())
    
            client.sock.send(b_request)
            logging.debug(f'Client sent data: {data}')


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


client = Client()
client.run()

logging.info(f'Client started and connected to {client.host.default}:{client.port.default}')

print('Welcome to geek-chat!')

try:
    read_thread = threading.Thread(target=client.read)
    read_thread.start()
    
    write_thread = threading.Thread(target=client.write)
    write_thread.start()
    
except KeyboardInterrupt:
    Client.sock.close()
    print('Client closed')