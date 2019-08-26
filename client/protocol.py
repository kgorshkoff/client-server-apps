from datetime import datetime


def make_request(username, action, data, token):
    result = {
        'username': username,
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data,
        'token': token
    }
    return result