from datetime import datetime
from protocol import make_response
from logs import log


def server_date_controller(request):
    response = make_response(request, 200, datetime.now().timestamp())
    log.logger.debug(f'Server date: {response.get("time")}')
    return make_response(request, 200, datetime.now().timestamp())
