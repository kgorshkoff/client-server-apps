import pytest
from datetime import datetime
from server.resolvers import resolve, get_server_actions
from server.echo.actions import echo_controller

@pytest.fixture
def data_fixture():
    return 'echo'

@pytest.fixture
def func_fixture():
    return echo_controller


def test_valid_resolve(data_fixture, func_fixture):
    actions = get_server_actions()
    assert type(actions.get(data_fixture)) == type(function)
