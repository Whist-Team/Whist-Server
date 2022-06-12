from unittest import TestCase
from unittest.mock import MagicMock

from whist.server.api.publish.events.event import Event
from whist.server.api.publish.subscriber import Subscriber


class SubscriberTestCase(TestCase):
    def setUp(self) -> None:
        self.connection_mock = MagicMock()
        self.subscriber = Subscriber(self.connection_mock)

    def test_send(self):
        event = Event()
        self.subscriber.send(event)
        self.connection_mock.send_json.assert_called_with(event)
