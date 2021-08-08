import unittest

from bson import ObjectId

from whist.server.database.user import UserInDb
from whist.server.services.error import UserNotFoundError
from whist.server.services.user_db_service import UserDatabaseService


class UserDbTestCase(unittest.TestCase):
    def setUp(self):
        self.user_database_service = UserDatabaseService()
        self.user: UserInDb = UserInDb(username='test', hashed_password='abc')

    def test_add_user(self):
        user_id = self.user_database_service.add(self.user)
        self.user.id = ObjectId(user_id)
        self.assertEqual(self.user, self.user_database_service.get(user_id))

    def test_user_not_existing(self):
        with self.assertRaises(UserNotFoundError):
            self.user_database_service.get('1' * 24)
