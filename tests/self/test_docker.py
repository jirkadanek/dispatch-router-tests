import pytest

import docker
import time


@pytest.fixture
def client(request):
    c = docker.Client()
    request.addfinalizer(c.close)
    print(c.version())
    return c


@pytest.fixture
def network(request, client: docker.Client):
    n = "mynetwork123"
    client.create_network(n)
    request.addfinalizer(lambda: client.remove_network(n))
    return n


class DispatchRouter(object):
    def __init__(self):
        pass

class TestDocker(object):
    def test_fixtures(self, network: str):
        time.sleep(10)
