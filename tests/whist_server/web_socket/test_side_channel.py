import asyncio
from unittest import TestCase
from unittest.mock import MagicMock, AsyncMock

from whist_core.user.player import Player

from whist_server.web_socket.events.event import PlayerJoinedEvent
from whist_server.web_socket.side_channel import SideChannel
from whist_server.web_socket.subscriber import Subscriber


class TestCase(TestCase):
    def setUp(self):
        self.connection_mock = MagicMock(send_json=AsyncMock())
        self.subscriber = Subscriber(self.connection_mock)
        player = Player(username='ititus', rating=100)
        self.event = PlayerJoinedEvent(player=player)
        self.side_channel = SideChannel()

    def test_send_joined(self):
        self.side_channel.attach(self.subscriber)
        asyncio.run(self.side_channel.notify(self.event))
        self.connection_mock.send_json.assert_called_with(
            {'name': self.event.name, 'event': self.event.model_dump()})

    def test_send_not_joined(self):
        asyncio.run(self.side_channel.notify(self.event))
        self.connection_mock.send_json.send_json.assert_not_called()

    def test_send_left(self):
        self.side_channel.attach(self.subscriber)
        self.side_channel.remove(self.subscriber)
        asyncio.run(self.side_channel.notify(self.event))
        self.connection_mock.send_json.send_json.assert_not_called()
