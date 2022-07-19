import unittest

from whist_core.user.player import Player

from whist_server.const import INITIAL_RATING
from whist_server.database.user import UserInDb
from whist_server.services.password import PasswordService


class UserInDbTestCase(unittest.TestCase):
    def setUp(self):
        password_service = PasswordService()
        self.user = UserInDb(username='test',
                             hashed_password=password_service.hash(
                                 'abc'))

    def test_verify_pwd(self):
        self.assertTrue(self.user.verify_password('abc'))

    def test_verify_fail(self):
        self.assertFalse(self.user.verify_password('bac'))

    def test_user(self):
        user = Player(username=self.user.username, rating=INITIAL_RATING)
        self.assertEqual(user, self.user.to_user())
