import asyncio
from unittest import TestCase
from unittest.mock import MagicMock, AsyncMock

from whist_server.web_socket.events.event import Event
from whist_server.web_socket.subscriber import Subscriber


class SubscriberTestCase(TestCase):
    def setUp(self) -> None:
        self.connection_mock = MagicMock(send_json=AsyncMock())
        self.subscriber = Subscriber(self.connection_mock)

    def test_send(self):
        event = Event()
        asyncio.run(self.subscriber.send(event))
        self.connection_mock.send_json.assert_called_with(
            {'name': event.name, 'event': event.dict()})
