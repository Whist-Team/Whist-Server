from tests.whist.server.base_player_test_case import BasePlayerTestCase
from whist.server.database.game import GameInDb
from whist.server.database.warning import PlayerAlreadyJoinedWarning
from whist.server.services.password import PasswordService


class GameInDbTestCase(BasePlayerTestCase):
    def setUp(self) -> None:
        super().setUp()
        password_service = PasswordService()
        self.game: GameInDb = GameInDb.create_with_pwd(game_name='test',
                                                       hashed_password=password_service.hash('abc'),
                                                       creator=self.player)
        self.assertEqual(['1'], self.game.players)

    def test_verify_pwd(self):
        self.assertTrue(self.game.verify_password('abc'))

    def test_verify_fail(self):
        self.assertFalse(self.game.verify_password('bac'))

    def test_verify_without_password(self):
        game: GameInDb = GameInDb.create_with_pwd(game_name='test', creator=self.player)
        self.assertTrue(game.verify_password(None))

    def test_join(self):
        self.assertTrue(self.game.join('2'))
        self.assertEqual(['1', '2'], self.game.players)
