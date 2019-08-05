from datetime import datetime
from server.protocol import make_response
from server.decorators import login_required


@login_required
def server_date_controller(request):
    response = make_response(request, 200, datetime.now().timestamp())
    return make_response(request, 200, datetime.now().timestamp())
