import sys
import hashlib
import json
import logging
import threading
import zlib
from socket import socket
from datetime import datetime
from protocol import make_request
from utils import get_chunk

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QTextEdit,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QPushButton)


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
        self._message_received = pyqtSignal(dict)
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
        # self._sock.close()
        return True

    @property
    def message_received(self):
        return self._message_receved

    def connect(self):
        try:
            self._sock.connect((self._host.default, self._port.default))
        except Exception as e:
            print(e)

    def read(self):
        while True:
            compressed_response = self._sock.recv(self._buffersize.default)
            encrypted_response = zlib.decompress(compressed_response)

            nonce, encrypted_response = get_chunk(encrypted_response, 16)
            key, encrypted_response = get_chunk(encrypted_response, 16)
            tag, encrypted_response = get_chunk(encrypted_response, 16)

            cipher = AES.new(key, AES.MODE_EAX, nonce)

            raw_response = cipher.decrypt_and_verify(encrypted_response, tag)
            logging.info(raw_response.decode())
            response = json.loads(raw_response)
            data = response.get('data')
            self.display_text.append(data)

            logging.debug(f'Client received response: {raw_response.decode()}')

    def render(self):
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setGeometry(400, 600, 400, 600)

        central_widget = QWidget()
        login_widget = QWidget()

        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)
        self.enter_text = QTextEdit()
        self.send_button = QPushButton('Send', window)
        self.enter_text.setMaximumHeight(64)
        self.send_button.setMaximumHeight(64)

        self.login = QTextEdit()
        self.password = QTextEdit()
        self.login_button = QPushButton('Login', login_window)
        self.register_button = QPushButton('Register', login_window)
        self.login.setMaximumHeight(64)
        self.password.setMaximumHeight(64)
        self.register_button.setMaximumHeight(64)
        self.login_button.setMaximumHeight(64)

        base_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        footer_layout = QHBoxLayout()

        login_top_layout = QVBoxLayout()
        login_footer_layout = QHBoxLayout()

        login_top_layout.addWidget(self.login)
        login_top_layout.addWidget(self.password)
        login_footer_layout.addWidget(self.login_button)
        login_footer_layout.addWidget(self.register_button_button)

        top_layout.addWidget(self.display_text)
        footer_layout.addWidget(self.enter_text)
        footer_layout.addWidget(self.send_button)

        base_layout.addLayout(top_layout)
        base_layout.addLayout(footer_layout)

        login_widget.setLayout(login_layout)
        login_window.setCentralWidget(login_widget)

        login_widget.show()

        central_widget.setLayout(base_layout)
        window.setCentralWidget(central_widget)

        dsk_widget = QDesktopWidget()
        geometry = dsk_widget.availableGeometry()
        center_position = geometry.center()
        frame_geometry = window.frameGeometry()
        frame_geometry.moveCenter(center_position)
        window.move(frame_geometry.topLeft())

        self.send_button.clicked.connect(self.write)

        # login_window.show()
        window.show()
        sys.exit(app.exec_())

    def write(self):
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX)

        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )
        token = hash_obj.hexdigest()

        data = self.enter_text.toPlainText()

        request = make_request('echo', {'data': data}, token)

        b_request = json.dumps(request).encode()
        encrypted_request, tag = cipher.encrypt_and_digest(b_request)

        b_request = zlib.compress(
            b'%(nonce)s%(key)s%(tag)s%(data)s' % {
                b'nonce': cipher.nonce, b'key': key, b'tag': tag, b'data': encrypted_request
            }
        )

        self.enter_text.clear()
        self._sock.send(b_request)
        logging.debug(f'Client sent data: {data}')

    def run(self):
        read_thread = threading.Thread(target=self.read)
        read_thread.start()

        logging.info(f'Client started and connected to {self._host.default}:{self._port.default}')

        self.render()
