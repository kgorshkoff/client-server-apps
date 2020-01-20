"""
Protocol API documentation
"""

from datetime import datetime


def make_request(action, data, token):
    result = {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data,
        'token': token
    }
    return result


def validate_request(raw):
    """
    Function for simple client request validation
    :param raw:
    :return:

    - Example::

            {'action': 'echo', 'time': 'timestamp'}
    """
    if 'action' in raw and 'time' in raw:
        return True
    return False


def make_response(request, code, data=None):
    """
    Creates dict response
    :param request: request itself
    :param code: http code
    :param data: any data sent by user
    :return:
    """
    return {
        'action': request.get('action'),
        'time': request.get('time'),
        'data': data,
        'code': code
    }
