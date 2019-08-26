import hashlib
import json
import logging
import threading
import zlib
from socket import socket
from datetime import datetime

from client.protocol import make_request


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


class Application:
    def __init__(self, args):
        self._host = TypedProperty('host', str, args.host if args.host else 'localhost')
        self._port = TypedProperty('port', int, args.port if args.port else 8000)
        self._buffersize = TypedProperty('buffersize', int, args.buffersize if args.buffersize else 1024)
        
        self._username = input('Enter your name: ')   
        self._sock = None

    
    def __enter__(self):
        if not self._sock:
            self._sock = socket()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Client shutdown'
        if exc_type:
            if not exc_type is KeyboardInterrupt:
                message = 'Client stopped with error'
        logging.info(message)
        self._sock.close()
        return True
    
    def connect(self):
        if not self._sock:
            self._sock = socket()
        self._sock.connect((self._host.default, self._port.default))
    
    def read(self):
        compressed_response = self._sock.recv(self._buffersize.default)
        b_response = zlib.decompress(compressed_response)
        response = b_response.decode()
        
        logging.debug(f'Client recieved response: {response}')
        
        if 'messenger' in response:
            json_response = json.loads(response)
            print(
                f"{datetime.fromtimestamp(json_response.get('time')).strftime('%H:%M:%S')} | \
                    {json_response.get('username')}: {json_response.get('data')}\n"
                )
        else:
            print(response)
    
    def write(self):
        action = input('Enter action: ')
        data = input('Enter data: ')
        
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )
        token = hash_obj.hexdigest()
        
        request = make_request(self._username, action, data, token)
        
        s_request = json.dumps(request)
        b_request = zlib.compress(s_request.encode())
        
        self._sock.send(b_request)
        logging.debug(f'Client sent data: {data}')
    
    def run(self):
        read_thread = threading.Thread(target=self.read)
        read_thread.start()

        while True:
            self.write()
            logging.info(f'Client started and connected to {self._host.default}:{self._port.default}')
            print('Welcome to geek-chat!')
