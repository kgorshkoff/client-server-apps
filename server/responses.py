import json
from datetime import datetime


def response_maker(status, text):
    if status < 400:
        result = {
            "response": status,
            "alert": text
        }
    else:
        result = {
            "response": status,
            "error": text
        }
    return json.dumps(result)


def form_response(request):
    if request['action'] == 'presence':
        return presence(request)

def presence(request):
    result = response_maker(200, f"User '{request['user']['account_name']}' is {request['user']['status']}")
    print(f"{datetime.utcfromtimestamp(request['time']).strftime('%Y-%m-%d %H:%M:%S')}: {result}")
    return result.encode()

def join(request):
    result = response_maker(200, f"User '{request['account_name']} has joined {request['room']}")
    return result.encode()