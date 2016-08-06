import pytest

import docker
import docker.utils
import subprocess
import socket
import time
import traceback
import contextlib


ROUTER_IMAGE = 'jdanekrh/dispatch-router:4-90415a'
SUBNET = '172.16.43.0/24'
RA = '172.16.43.2'

import docker
import subprocess


@pytest.fixture
def client(request):
    c = docker.Client()
    request.addfinalizer(c.close)
    print(c.version())
    return c


@pytest.fixture
def network(request, client: docker.Client):
    name = "dispatch"
    ipam_pool = docker.utils.create_ipam_pool(subnet=SUBNET)
    ipam_config = docker.utils.create_ipam_config(pool_configs=[ipam_pool])
    network = client.create_network(name, driver='bridge', ipam=ipam_config)
    net_id = network['Id']
    request.addfinalizer(lambda: client.remove_network(net_id))
    return net_id


class TestDocker(object):
    def test_fixtures(self, network: str):
        stdout = subprocess.run("docker network ls",
                                stdout=subprocess.PIPE,
                                universal_newlines=True, shell=True, check=True).stdout
        print(network)
        assert network[:6] in stdout

    @contextlib.contextmanager
    def container(self, client: docker.Client, network: str):
        container = None
        try:
            container = client.create_container(ROUTER_IMAGE, name="ra")
            client.connect_container_to_network(container, net_id=network, ipv4_address=RA)
            client.start(container)
            yield container
            client.kill(container)
        finally:
            if container is not None:
                client.remove_container(container)

    def test_run_container(self, client, network):
        with self.container(client, network) as container:
            subprocess.run(['ping', '-c1', RA], check=True)

    def test_run_qdstat(self, client: docker.Client, network):
        with self.container(client, network) as container:
            while True:
                try:
                    with socket.create_connection((RA, 5672)):
                        break
                except ConnectionRefusedError:
                    time.sleep(0.03)

            exec = client.exec_create(container, "qdstat -g")
            output = client.exec_start(exec).decode()
            print(output)
