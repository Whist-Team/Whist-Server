from bson import ObjectId

from tests.whist.server.base_player_test_case import BasePlayerTestCase
from whist.server.database import db
from whist.server.database.game import GameInDb
from whist.server.services.error import GameNotFoundError
from whist.server.services.game_db_service import GameDatabaseService


class GameDdServiceTestCase(BasePlayerTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.service = GameDatabaseService()
        self.game = GameInDb.create_with_pwd(game_name='test', hashed_password='abc',
                                             creator=self.player)

    def test_add(self):
        game_id = self.service.add(self.game)
        self.game.id = ObjectId(game_id)
        self.assertEqual(self.game, self.service.get(game_id))
        self.assertEqual(1, db.game.count_documents({}))

    def test_add_duplicate(self):
        game_id_first = self.service.add(self.game)
        game_id_second = self.service.add(self.game)
        self.assertEqual(game_id_first, game_id_second)

    def test_not_existing(self):
        game_id = '1' * 24
        error_msg = f'Game with id "{game_id}" not found.'
        with self.assertRaisesRegex(GameNotFoundError, error_msg):
            self.service.get(game_id)

    def test_get_by_name(self):
        game_id = self.service.add(self.game)
        self.game.id = ObjectId(game_id)
        self.assertEqual(self.game, self.service.get_by_name('test'))

    def test_save(self):
        game_id = self.service.add(self.game)
        self.game.id = game_id
        self.game.table.min_player = 3
        self.service.save(self.game)
        game = self.service.get(game_id)
        self.assertEqual(3, game.table.min_player)
