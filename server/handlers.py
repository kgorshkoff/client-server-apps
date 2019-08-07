import json
import logging

from server.middleware import compression_middleware, encryption_middleware
from server.resolvers import resolve
from server.protocol import make_response, validate_request


@compression_middleware
@encryption_middleware
def handle_default_request(raw_request):
    request = json.loads(raw_request.decode())

    if validate_request(request):
        action_name = request.get('action')
        controller = resolve(action_name)
        if controller:
            try:
                logging.debug(f'Controller {action_name} resolved with request: {raw_request.decode()}')
                response = controller(request)
            except Exception as err:
                logging.critical(f'Controller {action_name} error {err}')
                response = make_response(request, 500, 'Internal server error')
        else:
            logging.error(f'Controller {action_name} not found')
            response = make_response(request, 404, f'Action with name {action_name} is not supported')
    else:
        logging.error(f'Wrong controller request: {request}')
        response = make_response(request, 400, 'wrong request format')

    return json.dumps(response).encode()