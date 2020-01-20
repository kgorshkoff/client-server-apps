import select
import logging
import threading
from socket import socket


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
    def __init__(self, args, handler):
        self._host = TypedProperty('host', str, args.host if args.host else 'localhost')
        self._port = TypedProperty('port', int, args.port if args.port else 8000)
        self._buffersize = TypedProperty('buffersize', int, args.buffersize if args.buffersize else 1024)
        self._handler = handler

        self._sock = socket()
        self._requests = list()
        self._connections = list()

    def __enter__(self):
        if not self._sock:
            self._sock = socket()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Server shutdown'
        if exc_type:
            if exc_type is not KeyboardInterrupt:
                message = 'Server stopped with error'
        logging.info(message, exc_info=exc_val)
        self._sock.close()
        return True

    def accept(self):
        try:
            client, address = self._sock.accept()
        except Exception:
            pass
        else:
            self._connections.append(client)
            logging.info(f'Client connected: {address[0]}:{address[1]} | connections: {len(self._connections)}')

    def bind(self, backlog=5):
        if not self._sock:
            self._sock = socket()
        self._sock.bind((self._host.default, self._port.default))
        self._sock.settimeout(0)
        self._sock.listen(backlog)

    def read(self, sock):
        try:
            b_request = sock.recv(self._buffersize.default)
        except Exception as err:
            # self._connections.remove(sock)
            logging.critical('Read exception raised', exc_info=err)
        else:
            if b_request:
                self._requests.append(b_request)

    def write(self, sock, response):
        try:
            sock.send(response)
        except Exception as err:
            # self._connections.remove(sock)
            logging.critical('Write exception raised', exc_info=err)

    def run(self):
        try:
            logging.info(f'Server is running {self._host.default}:{self._port.default}')

            while True:
                self.accept()

                rlist, wlist, xlist = select.select(
                    self._connections, self._connections, self._connections, 0
                )

                for r_client in rlist:
                    r_thread = threading.Thread(
                        target=self.read, args=(r_client,)
                    )
                    r_thread.start()

                if self._requests:
                    b_request = self._requests.pop()
                    b_response = self._handler(b_request)

                    for w_client in wlist:
                        w_thread = threading.Thread(
                            target=self.write, args=(w_client, b_response)
                        )
                        w_thread.start()

        except KeyboardInterrupt:
            logging.info('Server shutting down')
