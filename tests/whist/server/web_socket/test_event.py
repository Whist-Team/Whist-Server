from unittest import TestCase

from whist.core.user.player import Player
from whist.server.web_socket.events.event import PlayerJoined


class EventTestCase(TestCase):
    def test_player_joined(self):
        player = Player(username='ititus', rating=100)
        expected_dict = {'player': player}

        event = PlayerJoined(player=player)
        self.assertEqual(expected_dict, dict(event))
