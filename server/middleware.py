import zlib
from functools import wraps


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
        #decrypt text
        b_response = func(request, *args, **kwargs)
        #encrypt text
        return b_response
    return wrapper