from protocol import make_response
from logs import log

def echo_controller(request):
    data = request.get('data')
    log.logger.debug(f'Echoing data: {data}')
    return make_response(request, 200, data)
