import unittest

from whist.server.database.game_info import GameInfo
from whist.server.services.game_info_db_service import GameInfoDatabaseService


class GameInfoDatabaseServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.service = GameInfoDatabaseService()
        self.info = GameInfo(game='whist', version='v1.0.0').copy(exclude={'id'})

    def test_add(self):
        self.service.add(self.info)
        self.assertEqual(self.info, self.service.get())
