from functools import reduce

from protocol import make_response
from decorators import logged
from database import Session, session_scope
from .models import Message


@logged
def echo_controller(request):
    data = request.get('data')
    message = Message(data=data)
    with session_scope() as db_session:
        db_session.add(message)

        response = make_response(request, 200, data)
        return response


def delete_message_controller(request):
    data = request.get('data')
    message_id = data.get('message_id')
    with session_scope() as db_session:
        message = db_session.query(Message).filter_by(id=message_id).first()
        db_session.delete(message)

        response = make_response(request, 200)
        return response


def update_message_controller(request):
    data = request.get('data')
    message_id = data.get('message_id')
    message_data = data.get('message_data')
    with session_scope() as db_session:
        message = db_session.query(Message).filter_by(id=message_id).first()
        message.data = message_data

        response = make_response(request, 200)
        return response


@logged
def get_messages_controller(request):
    with session_scope() as db_session:
        messages = reduce(
            lambda value, item: value + [{'data': item.data, 'created': item.created.timestamp()}],
            db_session.query(Message).all(),
            []
        )
        response = make_response(request, 200, messages)
        return response
