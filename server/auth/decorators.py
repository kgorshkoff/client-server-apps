from functools import wraps

from protocol import make_response
from database import session_scope
from .models import Session as Session


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'token' not in request:
            result = make_response(request, 403, 'Access denied')
            return result

        with session_scope() as db_session:
            user_session = db_session.query(Session).filter_by(token=request.get('token')).first()
            if not user_session or user_session.closed:
                result = make_response(request, 403, 'Access denied')
                return result

        return func(request, *args, **kwargs)
    return wrapper