# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import contextlib
import socket

import docker
import docker.utils
import pytest
import time

ROUTER_IMAGE = 'jdanekrh/dispatch-router:6-ae1223'
NETWORK_NAME = 'dispatch'
SUBNET = '172.16.43.0/24'
RA = '172.16.43.2'


@pytest.fixture(scope='session')
def client(request):
    c = docker.Client()
    request.addfinalizer(c.close)
    print(c.version())
    return c


@pytest.fixture(scope='session')
def network(request, client: docker.Client):
    ipam_pool = docker.utils.create_ipam_pool(subnet=SUBNET)
    ipam_config = docker.utils.create_ipam_config(pool_configs=[ipam_pool])
    network = client.create_network(NETWORK_NAME, driver='bridge', ipam=ipam_config)
    net_id = network['Id']
    request.addfinalizer(lambda: client.remove_network(net_id))
    return net_id


@contextlib.contextmanager
def create_container(client: docker.Client, network: str):
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


def wait_for_port(host, port, timeout=5.0):
    t = 0.03
    while True:
        try:
            with socket.create_connection((host, port)):
                break
        except ConnectionRefusedError:
            time.sleep(t)
            timeout -= t
        if timeout <= 0.0:
            raise TimeoutError()
    return True
