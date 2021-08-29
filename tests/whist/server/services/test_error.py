from unittest import TestCase

from whist.server.services.error import UserNotFoundError


class UserNotFoundTestCase(TestCase):
    def test_user_not_found_error(self):
        error = UserNotFoundError()
        self.assertEqual('User not found.', error.args[0])
