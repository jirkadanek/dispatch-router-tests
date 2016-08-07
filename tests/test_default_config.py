import inspect
import random
import string
import threading
import time

import docker
import proton
import pytest
# from proton import Message
#
# from dispatch.test_single_router import *
# from dispatch.test_multiple_routers import rd_ip, ba_ip
#
# from remote import AnsibleRemote
# import clients.python_qpid_proton as proton
#
# FIXME(jdanek): I was overusing threading module, I did not know better then
# import threading
# import itertools
#
# from unittest import TestCase

# START_ROUTERS = True
# START_ROUTERS = False

from .conftest import RA, create_container, wait_for_port


@pytest.yield_fixture(scope='module')
def router(client: docker.Client, network: str):
    with create_container(client, network) as c:
        yield c


class TestDefaultConfig(object):
    @pytest.fixture(scope='module', autouse=True)
    def setup(self, router):
        self.router = router

    def test_start_and_stop_router(self):
        wait_for_port(RA, 5672)

    def test_send_and_receive_a_message(self):
        address = "amqp://{}/{}".format(RA, ''.join(random.sample(string.ascii_letters, 8)))
        message = u"This is a test message."

        class Sender(threading.Thread):
            def run(self):
                messenger = proton.Messenger()
                messenger.put(proton.Message(body=message, address=address))
                messenger.send()
                messenger.stop()

        sender = Sender()
        sender.start()

        received_message = proton.Message()
        messenger = proton.Messenger()
        messenger.subscribe(address)
        messenger.recv()
        if messenger.incoming:
            messenger.get(received_message)
        messenger.stop()
        sender.join()

        assert message == received_message.body

    def test_send_direct_message(self):
        message = u'test_send_direct_message'

        receiver = proton.Messenger()
        subscription = receiver.subscribe('amqp://{}/#'.format(RA))
        address = subscription.address

        address = address.replace('amqp:/', 'amqp://{}/'.format(RA))

        sender = proton.Messenger()
        sender.put(proton.Message(message, address=address))
        sender.send()

        received_message = proton.Message()
        receiver.recv()
        if receiver.incoming:
            receiver.get(received_message)
        receiver.stop()
        sender.stop()

        assert message == received_message.body
