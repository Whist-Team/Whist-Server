from unittest import TestCase

from whist.core.user.player import Player
from whist.server.web_socket.events.event import PlayerJoinedEvent


class EventTestCase(TestCase):
    def test_player_joined(self):
        player = Player(username='ititus', rating=100)
        event = PlayerJoinedEvent(player=player)
        self.assertIsNotNone(event.json())

    def test_player_joined_name(self):
        player = Player(username='ititus', rating=100)
        event = PlayerJoinedEvent(player=player)
        self.assertEqual('PlayerJoinedEvent', event.name)
