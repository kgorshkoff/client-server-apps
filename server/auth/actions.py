from .controllers import create_user_controller, read_user_controller, update_user_controller, delete_user_controller


actionnames = [
    {'action': 'create_user', 'controller': create_user_controller},
    {'action': 'read_user', 'controller': read_user_controller},
    {'action': 'update_user', 'controller': update_user_controller},
    {'action': 'delete_user', 'controller': delete_user_controller},
]
