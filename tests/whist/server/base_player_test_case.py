from unittest import TestCase

from whist.core.user.player import Player

from whist.server.const import INITIAL_RATING


class BasePlayerTestCase(TestCase):
    def setUp(self) -> None:
        self.player = Player(username='test', rating=INITIAL_RATING)
