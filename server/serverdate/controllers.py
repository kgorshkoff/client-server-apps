from datetime import datetime
from protocol import make_response
import logging


def server_date_controller(request):
    request['username'] = 'Server'
    response = make_response(request, 200, datetime.now().timestamp())
    logging.debug(f'Server date: {response.get("time")}')
    return response
