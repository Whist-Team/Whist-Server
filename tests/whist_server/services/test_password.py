import unittest

from whist_server.services.password import PasswordService

PASSWORD = 'abc'


class PasswordServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.pwd_service = PasswordService()
        self.hashed_password = self.pwd_service.hash(PASSWORD)

    def test_verify_true(self):
        self.assertTrue(self.pwd_service.verify(PASSWORD, self.hashed_password))

    def test_verify_false(self):
        self.assertFalse(self.pwd_service.verify(PASSWORD, 'a'))
