# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import contextlib
import docker
import docker.utils
import subprocess
import pytest
import socket
import time
import traceback

from ..conftest import ROUTER_IMAGE, RA, create_container, wait_for_port


class TestDocker(object):
    def test_fixtures(self, network: str):
        stdout = subprocess.run("docker network ls",
                                stdout=subprocess.PIPE,
                                universal_newlines=True, shell=True, check=True).stdout
        print(network)
        assert network[:6] in stdout

    def test_run_container(self, client, network):
        with create_container(client, network):
            subprocess.run(['ping', '-c1', RA], check=True)

    def test_run_qdstat(self, client: docker.Client, network):
        with create_container(client, network) as container:
            wait_for_port(RA, 5672)
            exec = client.exec_create(container, "qdstat -g")
            output = client.exec_start(exec).decode()
            print(output)

    def container(self, client, network):
        return conftest.container