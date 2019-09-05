from functools import wraps
from Crypto.Cipher import AES

from .utils import get_chunk
from .settings import MESSAGE_PATTERN


def encryption_middleware(func):
    @wraps(func)
    def wrapper(encrypted_request, *args, **kwargs):
        nonce, encrypted_request = get_chunk(encrypted_request, 16)
        key, encrypted_request = get_chunk(encrypted_request, 16)
        tag, encrypted_request = get_chunk(encrypted_request, 16)

        cipher = AES.new(key, AES.MODE_EAX, nonce)

        raw_request = cipher.decrypt_and_verify(encrypted_request, tag)
        response = func(raw_request, *args, **kwargs)

        cipher = AES.new(key, AES.MODE_EAX)
        encrypted_response, tag = cipher.encrypt_and_digest(response)
        result = MESSAGE_PATTERN % {b'nonce': cipher.nonce, b'key': key, b'tag': tag, b'data': encrypted_response}
        return result
    return wrapper


# def auth_middleware(func):
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         request_obj = json.loads(request)
#         login = request_obj.get('login')
#         token = request_obj.get('token')
#         time = request_obj.get('time')
#
#         session = Session()
#         user = session.query(User).filter_by(name=login).first()
#
#         if user:
#             digest = hmac.new(time, user.password)
#             authenticated = hmac.compare_digest(digest, token)
#
#         if authenticated:
#             b_response = func(request, *args, **kwargs)
#             return b_response
#         else:
#             response = make_response(request, 401, 'Access denied')
#             b_response = json.dumps(response).encode()
#             return b_response
#     return wrapper