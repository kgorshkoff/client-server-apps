from datetime import datetime


def make_request(action, data, token):
    result = {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data,
        'token': token
    }
    return result
