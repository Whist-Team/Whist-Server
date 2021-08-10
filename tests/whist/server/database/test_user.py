import unittest

from whist.server.database.user import UserInDb, User
from whist.server.services.password import PasswordService


class UserInDbTestCase(unittest.TestCase):
    def setUp(self):
        password_service = PasswordService()
        self.user = UserInDb(username='test', hashed_password=password_service.hash('abc'))

    def test_verify_pwd(self):
        self.assertTrue(self.user.verify_password('abc'))

    def test_verify_fail(self):
        self.assertFalse(self.user.verify_password('bac'))

    def test_user(self):
        user = User(id=self.user.id, username=self.user.username)
        self.assertEqual(user, self.user.to_user())
