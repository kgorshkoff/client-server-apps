from server.database import Session
from .models import User
from server.protocol import make_response


def create_user_controller(request):
    data = request.get('data')
    username = request.get('username')
    
    session = Session()
    message = User(username=username, password=data)
    session.add(message)
    session.commit()
    
    return make_response(request, 200, data)


def read_user_controller(request):
    data = request.get('data')

    session = Session()
    query = session.query(User, data)
    
    return make_response(request, 200, query)


def update_user_controller(request):
    pass


def delete_user_controller(request):
    data = request.get('data')

    session = Session()
    session.query(User, data).delete()
    session.commit()
    
    return make_response(request, 200, 'Deleted')