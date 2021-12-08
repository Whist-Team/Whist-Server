import unittest

from whist.server.database import db
from whist.server.database.user import UserInDb
from whist.server.services.error import UserNotFoundError, UserExistsError
from whist.server.services.user_db_service import UserDatabaseService


class UserDbTestCase(unittest.TestCase):
    def setUp(self):
        self.user_database_service = UserDatabaseService()
        self.user: UserInDb = UserInDb(username='test', hashed_password='abc')
        db.user.drop()

    def tearDown(self) -> None:
        db.user.drop()

    def test_add_user(self):
        self.assertTrue(self.user_database_service.add(self.user))
        self.assertEqual(self.user, self.user_database_service.get(self.user.username))

    def test_user_not_existing(self):
        username = '1'
        error_msg = f'User with name "{username}" not found.'
        with self.assertRaisesRegex(UserNotFoundError, error_msg):
            self.user_database_service.get(username)

    def test_unique_user(self):
        _ = self.user_database_service.add(self.user)
        with(self.assertRaises(UserExistsError)):
            _ = self.user_database_service.add(self.user)
        self.assertEqual(1, db.user.estimated_document_count())
