import pytest

from day4.api.server import ApiServer


@pytest.fixture(scope="session")
def api_server():
    server = ApiServer().start()
    yield server
    server.stop()


@pytest.fixture(scope="session")
def base_url(api_server):
    return api_server.base_url
