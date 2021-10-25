import unittest

from whist.server.database.game import GameInDb
from whist.server.services.password import PasswordService


class GameInDbTestCase(unittest.TestCase):
    def setUp(self) -> None:
        password_service = PasswordService()
        self.game: GameInDb = GameInDb(game_name='test',
                                       hashed_password=password_service.hash('abc'),
                                       creator='1')
        self.assertEqual(['1'], self.game.players)

    def test_verify_pwd(self):
        self.assertTrue(self.game.verify_password('abc'))

    def test_verify_fail(self):
        self.assertFalse(self.game.verify_password('bac'))

    def test_verify_without_password(self):
        game: GameInDb = GameInDb(game_name='test', creator='1')
        self.assertTrue(game.verify_password(None))

    def test_join(self):
        self.assertTrue(self.game.join('2'))
        self.assertEqual(['1', '2'], self.game.players)
