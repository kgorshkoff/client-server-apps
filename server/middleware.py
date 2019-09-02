import hmac
import zlib
import json
from functools import wraps
from Crypto.Cipher import AES

from protocol import make_response
from auth.models import User
from database import Session


def compression_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        b_request = zlib.decompress(request)
        b_response = func(b_request, *args, **kwargs)
        result = zlib.compress(b_response)
        return result
    return wrapper


def encryption_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        encrypted_request = json.loads(request)

        key = encrypted_request.get('key')
        data = encrypted_request.get('data')
        cipher = AES.new(key, AES.MODE_CDC)

        decrypted_data = cipher.decrypt(data)
        decrypted_request = encrypted_request.copy()
        decrypted_request[data] = decrypted_data
        bytes_request = json.dump(decrypted_request).encode()

        b_response = func(bytes_request, *args, **kwargs)

        decrypted_response = json.loads(b_response)
        decrypted_data = decrypted_response.get('data')
        encrypted_data = cipher.encrypt(decrypted_data)
        encrypted_response = decrypted_response.copy()
        encrypted_response[data] = encrypted_data

        response = json.dumps(encrypted_response).encode()

        return response
    return wrapper


def auth_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        request_obj = json.loads(request)
        login = request_obj.get('login')
        token = request_obj.get('token')
        time = request_obj.get('time')

        session = Session()
        user = session.query(User).filter_by(name=login).first()

        if user:
            digest = hmac.new(time, user.password)
            authenticated = hmac.compare_digest(digest, token)

        if authenticated:
            b_response = func(request, *args, **kwargs)
            return b_response
        else:
            response = make_response(request, 401, 'Access denied')
            b_response = json.dumps(response).encode()
            return b_response
    return wrapper
