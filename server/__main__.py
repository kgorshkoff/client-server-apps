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

        
class Server:
    def __init__(self):
        self._host = TypedProperty('host', str, args.host if args.host else 'localhost')
        self._port = TypedProperty('port', int, args.port if args.port else 8000)
        self._buffersize = TypedProperty('buffersize', int, args.buffersize if args.buffersize else 1024)
        self._log_path = TypedProperty('log_path', str, os.getcwd() + '/logs/' + datetime.today().strftime("%Y%m%d") + '_server_main.log')
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self._log_path.default), logging.StreamHandler()
            ]
        )

    requests = []
    connections = []
    
    def run(self):
        self.sock = socket()
        self.sock.bind((self._host.default, self._port.default))
        self.sock.settimeout(0)
        self.sock.listen(5)

    def read(self, sock):
        try:
            b_request = sock.recv(self._buffersize.default)
        except Exception:
            self.connections.remove(sock)
        else:
            if b_request:
                self.requests.append(b_request)

    def write(self, sock, response):
        try:
            sock.send(response)
        except Exception:
            self.connections.remove(sock)


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
    required=False, help='set server buffersize'
)
args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        for k, v in file_config.items():
            args.__setattr__(k, v)


try:
    server = Server()
    server.run()

    logging.info(f'Server is running {server._host.default}:{server._port.default}')

    while True:
        try:
            client, address = server.sock.accept()
            server.connections.append(client)
            logging.info(f'Client connected: {address[0]}:{address[1]} | connections: {len(server.connections)}')
        except:
            pass

        rlist, wlist, xlist = select.select(
            server.connections, server.connections,  server.connections, 0
        )

        for r_client in rlist:
            r_thread = threading.Thread(
                target=server.read, args=(r_client, )
                )
            r_thread.start()

        if server.requests:
            b_request = server.requests.pop()
            b_response = handle_default_request(b_request)

            for w_client in wlist:
                w_thread = threading.Thread(
                target=server.write, args=(w_client, b_response)
                )
                w_thread.start()


except KeyboardInterrupt:
    logging.info('Server shutting down')
