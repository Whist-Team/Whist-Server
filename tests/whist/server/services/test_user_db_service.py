import unittest

from bson import ObjectId

from whist.server.database import db
from whist.server.database.user import UserInDb
from whist.server.services.error import UserNotFoundError
from whist.server.services.user_db_service import UserDatabaseService


class UserDbTestCase(unittest.TestCase):
    def setUp(self):
        self.user_database_service = UserDatabaseService()
        self.user: UserInDb = UserInDb(username='test', hashed_password='abc')

    def tearDown(self) -> None:
        db.user.drop()

    def test_add_user(self):
        user_id = self.user_database_service.add(self.user)
        self.user.id = ObjectId(user_id)
        self.assertEqual(self.user, self.user_database_service.get(user_id))

    def test_user_not_existing(self):
        user_id = '1' * 24
        error_msg = f'User with id "{user_id}" not found.'
        with self.assertRaisesRegex(UserNotFoundError, error_msg):
            self.user_database_service.get(user_id)

    def test_user_by_name(self):
        user_id = self.user_database_service.add(self.user)
        self.user.id = ObjectId(user_id)
        self.assertEqual(self.user, self.user_database_service.get_by_name(self.user.username))

    def test_user_by_name_not_existing(self):
        username = '1'
        error_msg = f'User with name "{username}" not found.'
        with self.assertRaisesRegex(UserNotFoundError, error_msg):
            self.user_database_service.get_by_name(username)
