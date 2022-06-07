import unittest

from whist.server.database import db
from whist.server.database.user import UserInDb
from whist.server.services.user_db_service import UserDatabaseService


class UserBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.user_database_service = UserDatabaseService()
        self.user: UserInDb = UserInDb(username='test', hashed_password='abc')
        db.user.drop()

    def tearDown(self) -> None:
        db.user.drop()
