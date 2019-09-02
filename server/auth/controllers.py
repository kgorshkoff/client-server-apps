from database import Session
from auth.models import User
from protocol import make_response


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
    query = session.query(User).filter_by('name')
    
    return make_response(request, 200, query)


def update_user_controller(request):
    user_id = request.get('user_id')
    user_password = request.get('user_password')
    session = Session()
    query = session.query(User).filter(id=user_id).get()
    query.password = user_password
    return 


def delete_user_controller(request):
    data = request.get('data')

    session = Session()
    session.query(User).filter_by('name').delete()
    session.commit()
    
    return make_response(request, 200, 'Deleted')