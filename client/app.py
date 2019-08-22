import hashlib
import json
import logging
import threading
import zlib
from socket import socket
from datetime import datetime


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
    def __init__(self, args):
        self._host = TypedProperty('host', str, args.host if args.host else 'localhost')
        self._port = TypedProperty('port', int, args.port if args.port else 8000)
        self._buffersize = TypedProperty('buffersize', int, args.buffersize if args.buffersize else 1024)
        
        self._sock = socket()
        self._username = input('Enter your name: ')   
    
    def read(self):
        while True:
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
        while True:
            action = input('Enter action: ')
            data = input('Enter data: ')
            
            hash_obj = hashlib.sha256()
            hash_obj.update(
                str(datetime.now().timestamp()).encode()
            )
            
            request = {
                'username': self._username,
                'action': action,
                'time': datetime.now().timestamp(),
                'data': data,
                'token': hash_obj.hexdigest()
            }
            
            s_request = json.dumps(request)
            b_request = zlib.compress(s_request.encode())
            
            self._sock.send(b_request)
            logging.debug(f'Client sent data: {data}')
    
    def run(self):
        try:
            self._sock.connect((self._host.default, self._port.default))
        except KeyboardInterrupt:
            Client.sock.close()
            print('Client closed')
        else:
            logging.info(f'Client started and connected to {self._host.default}:{self._port.default}')
            print('Welcome to geek-chat!')
            read_thread = threading.Thread(target=self.read)
            read_thread.start()
            
            write_thread = threading.Thread(target=self.write)
            write_thread.start()
