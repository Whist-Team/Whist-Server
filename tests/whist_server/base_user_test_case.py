import unittest

from whist_server.const import INITIAL_RATING
from whist_server.database import db
from whist_server.database.user import UserInDb
from whist_server.services.user_db_service import UserDatabaseService


class UserBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.user_database_service = UserDatabaseService()
        self.user: UserInDb = UserInDb(username='test', hashed_password='abc')
        self.second_user = UserInDb(username='lower_ranking', rating=INITIAL_RATING - 10,
                                    hashed_password='abc')
        db.user.drop()

    def tearDown(self) -> None:
        db.user.drop()
