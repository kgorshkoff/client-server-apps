from protocol import make_response
from logs import log

def server_error_controller(request):
    log.logger.debug('User generated server error')
    raise Exception('Server error message')
