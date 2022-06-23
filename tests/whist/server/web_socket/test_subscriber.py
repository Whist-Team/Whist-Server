from unittest import TestCase
from unittest.mock import MagicMock, patch

from whist.server.web_socket.events.event import Event
from whist.server.web_socket.subscriber import Subscriber


class SubscriberTestCase(TestCase):
    def setUp(self) -> None:
        self.connection_mock = MagicMock()
        self.subscriber = Subscriber(self.connection_mock)

    @patch('asyncio.run')
    def test_send(self, run_mock):
        event = Event()
        self.subscriber.send(event)
        run_mock.assert_called_with(
            self.connection_mock.send_json({'name': event.name, 'event': event.json()}))
