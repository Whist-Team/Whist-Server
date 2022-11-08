import pytest

from tests.whist_server.base_user_test_case import UserBaseTestCase
from whist_server.database import db
from whist_server.services.error import UserNotFoundError, UserExistsError


@pytest.mark.integtest
class UserDbTestCase(UserBaseTestCase):

    def test_add_user(self):
        user_id = self.user_database_service.add(self.user)
        self.assertTrue(user_id)
        self.assertEqual(self.user, self.user_database_service.get(user_id))

    def test_user_not_existing(self):
        user_id = '5' * 24
        with self.assertRaises(UserNotFoundError):
            self.user_database_service.get(user_id)

    def test_get_name_user_not_existing(self):
        username = 'fake'
        error_msg = f'User with name "{username}" not found.'
        with self.assertRaisesRegex(UserNotFoundError, error_msg):
            self.user_database_service.get_by_username(username)

    def test_unique_user(self):
        _ = self.user_database_service.add(self.user)
        with(self.assertRaises(UserExistsError)):
            _ = self.user_database_service.add(self.user)
        self.assertEqual(1, db.user.estimated_document_count())

    def test_from_github(self):
        github_id = '123'
        github_name = 'choco'
        self.user.github_id = github_id
        self.user.github_username = github_name
        _ = self.user_database_service.add(self.user)
        return_user = self.user_database_service.get_from_github(github_id)
        self.assertEqual(self.user, return_user)

    def test_from_github_nouser(self):
        github_name = 'not'
        with self.assertRaises(UserNotFoundError):
            return_user = self.user_database_service.get_from_github(github_name)
