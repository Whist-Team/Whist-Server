from unittest import TestCase

from whist.core.user.player import Player
from whist.server.web_socket.events.event import PlayerJoinedEvent


class EventTestCase(TestCase):
    def setUp(self) -> None:
        self.player = Player(username='ititus', rating=100)

    def test_player_joined(self):
        event = PlayerJoinedEvent(player=self.player)
        self.assertIsNotNone(event.json())

    def test_player_joined_name(self):
        event = PlayerJoinedEvent(player=self.player)
        self.assertEqual('PlayerJoinedEvent', event.name)
