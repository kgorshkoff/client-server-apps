import json
import datetime


def authenticate(account, password):
    result = {
        "action": "authenticate",
        "time": datetime.datetime.now().timestamp(),
                "user": {
                        "account_name": account,
                        "password":     password
                }
    }
    
    return json.dumps(result)


def presence(account): 
    result = {
        "action": "presence",
        "time": datetime.datetime.now().timestamp(),
        "type": "status",
        "user": {
                "account_name": account,
                "status":       "Online!"
        }
    }
    return json.dumps(result)


def msg(from_account, to_account, message, encoding='ascii'):
    result = {
        "action": "msg",
        "time": datetime.datetime.now().timestamp(),
        "to": from_account,
        "from": from_account,
        "encoding": encoding,
        "message": message
    }
    return result


def join(account, room):
    result = {
        "action": "join",
        "account_name": account,
        "time": datetime.datetime.now().timestamp(),
        "room": room
    }
    return json.dumps(result)


def leave(account, room):
    result = {
        "action": "leave",
        "account_name": account,
        "time": datetime.datetime.now().timestamp(),
        "room": room
    }
    return json.dumps(result)


def quit():
    result = {
        "action": "quit",
        "time": datetime.datetime.now().timestamp()
    }
    return json.dumps(result)
