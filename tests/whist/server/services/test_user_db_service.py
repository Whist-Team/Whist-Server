from tests.whist.server.base_user_test_case import UserBaseTestCase
from whist.server.database import db
from whist.server.services.error import UserNotFoundError, UserExistsError


class UserDbTestCase(UserBaseTestCase):

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
