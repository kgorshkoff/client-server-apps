from datetime import datetime
from server.protocol import make_response
import logging


def server_date_controller(request):
    response = make_response(request, 200, datetime.now().timestamp())
    logging.debug(f'Server date: {response.get("time")}')
    return make_response(request, 200, datetime.now().timestamp())
