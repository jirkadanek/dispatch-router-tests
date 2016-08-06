import pytest

import docker
import time


@pytest.fixture
def client(request):
    c = docker.Client(version='1.20')
    request.addfinalizer(c.close)
    print(c.version())
    return c


@pytest.fixture
def network(request, client: docker.Client):
    network = "mynetwork123"
    client.create_network(network)
    request.addfinalizer(lambda: client.remove_network(network))
    return network


class DispatchRouter(object):
    def __init__(self):
        pass

class TestDocker(object):
    def test_fixtures(self, network: str):
        time.sleep(10)
