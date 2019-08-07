import pytest
from datetime import datetime
from server.resolvers import resolve, get_server_actions
from server.settings import INSTALLED_MODULES


exceptions = ['servererrors']

@pytest.fixture
def modules_fixture():
    return INSTALLED_MODULES

def test_valid_resolve(modules_fixture):
    actions = get_server_actions()
    for module in modules_fixture:
        if module not in exceptions:
            assert callable(actions.get(module)) == True
