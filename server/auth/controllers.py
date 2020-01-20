import hmac
from database import Session, session_scope
from auth.models import User
from datetime import datetime

from decorators import login_required
from protocol import make_response

from .utils import authenticate, login
from .settings import SECRET_KEY


def login_controller(request):
    errors = {}
    is_valid = True
    data = request.get('data')

    if 'time' not in request:
        errors.update({'time': 'Attribute is required'})
        is_valid = False
    if 'login' not in request:
        errors.update({'login': 'Attribute is required'})
        is_valid = False
    if 'password' not in request:
        errors.update({'password': 'Attribute is required'})
        is_valid = False

    if not is_valid:
        response = make_response(request, 400, errors)
        return response

    user = authenticate(data.get('login'), data.get('password'))

    if user:
        token = login(request, user)
        response = make_response(request, 200, {'token': token})
        return response

    response = make_response(request, 400, 'Enter correct login and password')
    return response


def registration_controller(request):
    errors = {}
    is_valid = True
    data = request.get('data')

    if 'login' not in data:
        errors.update({'login': 'Attribute is required'})
        is_valid = False
    if 'password' not in data:
        errors.update({'password': 'Attribute is required'})
        is_valid = False

    if not is_valid:
        response = make_response(request, 400, errors)
        return response

    hmac_obj = hmac.new(SECRET_KEY.encode(), data.get('password').encode())
    password_digest = hmac_obj.digest()

    with session_scope() as db_session:
        user = User(name=data.get('login'), password=password_digest)
        db_session.add(user)
    token = login(request, user)
    response = make_response(request, 200, {'token': token})
    return response


@login_required
def logout_controller(request):
    with session_scope() as db_session:
        user_session = db_session.query(Session).filter_by(token=request.get('token')).first()
        user_session.closed = datetime.now()

        response = make_response(request, 200, 'Session closed')
        return response
