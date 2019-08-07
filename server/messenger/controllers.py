from server.protocol import make_response
from server.decorators import logged


# @logged
def messenger_controller(request):
    data = request.get('data')
    return make_response(request, 200, data)
