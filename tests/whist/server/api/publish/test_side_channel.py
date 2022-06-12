from unittest import TestCase
from unittest.mock import MagicMock

from whist.server.api.publish.events.event import Event
from whist.server.api.publish.side_channel import SideChannel
from whist.server.api.publish.subscriber import Subscriber


class TestCase(TestCase):
    def setUp(self):
        self.connection_mock = MagicMock()
        self.subscriber = Subscriber(self.connection_mock)
        self.event = Event()
        self.side_channel = SideChannel()

    def test_send_joined(self):
        self.side_channel.attach(self.subscriber)
        self.side_channel.notify(self.event)
        self.connection_mock.send_json.assert_called_with(self.event)

    def test_send_not_joined(self):
        self.side_channel.notify(self.event)
        self.connection_mock.send_json.assert_not_called()

    def test_send_left(self):
        self.side_channel.attach(self.subscriber)
        self.side_channel.remove(self.subscriber)
        self.side_channel.notify(self.event)
        self.connection_mock.send_json.assert_not_called()
