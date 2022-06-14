from unittest import TestCase
from unittest.mock import MagicMock

from whist.server.web_socket.events.event import PlayerJoined


class EventTestCase(TestCase):
    def test_player_joined(self):
        player = MagicMock()
        expected_dict = {'player': player}

        event = PlayerJoined(player)

        self.assertEqual(expected_dict, dict(event))
