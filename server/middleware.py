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

