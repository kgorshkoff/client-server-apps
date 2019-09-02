import os 


INSTALLED_MODULES = (
    'auth',
    'echo',
    'security',
    'messenger',
    'serverdate',
    'servererrors',
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONNECTION_STRING = f'sqlite:///{os.path.dirname(os.path.abspath(__file__))}/sqlite.db'
