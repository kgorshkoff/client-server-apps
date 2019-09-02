import sys
import hashlib
import json
import logging
import threading
import zlib
from socket import socket
from datetime import datetime
from protocol import make_request

from Crypto.Cipher import AES
from utils import get_chunk


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
        self._host = TypedProperty('host', str, args.host if args.host else '0.0.0.0')
        self._port = TypedProperty('port', int, args.port if args.port else 8000)
        self._buffersize = TypedProperty('buffersize', int, args.buffersize if args.buffersize else 1024)
        
        self._username = input('Enter your name: ')   
        self._sock = socket()

    def __enter__(self):
        self._sock.connect((self._host.default, self._port.default))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Client shutdown'
        if exc_type:
            if exc_type is not KeyboardInterrupt:
                message = 'Client stopped with error'
        logging.info(message, exc_info=exc_val)
        self._sock.close()
        return True
    
    def connect(self):
        try:
            self._sock.connect((self._host.default, self._port.default))
        except Exception as e:
            print(e)

    def read(self):
        compressed_response = self._sock.recv(self._buffersize.default)
        encrypted_response = zlib.decompress(compressed_response)

        nonce, encrypted_response = get_chunk(encrypted_response, 16)
        key, encrypted_response = get_chunk(encrypted_response, 16)
        tag, encrypted_response = get_chunk(encrypted_response, 16)

        cipher = AES.new(key, AES.MODE_EAX, nonce)

        raw_response = cipher.decrypt_and_verify(encrypted_response, tag)
        response = raw_response.decode()
        
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
        key = get_random_bytes(16)
        cipher = AES.key(key, AES.MODE_EAX)

        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )
        token = hash_obj.hexdigest()

        action = input('Enter action: ')
        data = input('Enter data: ')

        request = make_request(self._username, action, data, token)

        b_request = json.dumps(request).encode()
        encrypted_request = cipher.encrypt_and_digest(b_request)

        b_request = zlib.compress(
            b'%(nonce)s%(key)s%(tag)s%(data)s' % {
                b'nonce': cipher.nonce, b'key': key, b'tag': tag, b'data': encrypted_request
            }
        )

        self._sock.send(b_request)
        logging.debug(f'Client sent data: {data}')

    def run(self):
        read_thread = threading.Thread(target=self.read)
        read_thread.start()

        logging.info(f'Client started and connected to {self._host.default}:{self._port.default}')

        while True:
            self.write()
