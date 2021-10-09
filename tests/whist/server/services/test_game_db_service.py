from unittest import TestCase

from bson import ObjectId

from whist.server.database.game import GameInDb
from whist.server.services.error import GameNotFoundError
from whist.server.services.game_db_service import GameDatabaseService


class GameDdServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.service = GameDatabaseService()
        self.game = GameInDb(game_name='test', hashed_password='abc')

    def test_add(self):
        game_id = self.service.add(self.game)
        self.game.id = ObjectId(game_id)
        self.assertEqual(self.game, self.service.get(game_id))

    def test_not_existing(self):
        game_id = '1' * 24
        error_msg = f'Game with id "{game_id}" not found.'
        with self.assertRaisesRegex(GameNotFoundError, error_msg):
            self.service.get(game_id)
