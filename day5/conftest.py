import pytest

from day5.server import FixtureServer


@pytest.fixture(scope="session")
def fixture_server():
    server = FixtureServer().start()
    yield server
    server.stop()


@pytest.fixture(scope="session")
def fixture_url(fixture_server):
    return fixture_server.base_url
