from unittest.mock import patch

from tests.whist_server.base_token_case import TestCaseWithToken
from whist_server.services.error import UserNotFoundError


class AuthTestCase(TestCaseWithToken):
    def setUp(self) -> None:
        super().setUp()
        self.login_creds = {'username': 'marcel', 'password': 'abc'}

    def test_auth_user(self):
        with patch('whist_server.services.authentication.check_credentials',
                   return_value=True):
            response = self.client.post(url='/user/auth', json=self.login_creds)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertTrue('access_token' in response.json())

    def test_wrong_password(self):
        with patch('whist_server.services.authentication.check_credentials',
                   return_value=False):
            response = self.client.post(url='/user/auth',
                                        json={'username': 'marcel', 'password': 'abcd'})
        self.assertEqual(response.status_code, 401, msg=response.content)
        self.assertFalse('access_token' in response.json())

    def test_no_password(self):
        response = self.client.post(url='/user/auth', json={'username': 'marcel'})
        self.assertEqual(response.status_code, 422, msg=response.content)
        self.assertFalse('access_token' in response.json())

    def test_no_username(self):
        response = self.client.post(url='/user/auth', json={'password': 'abc'})
        self.assertEqual(response.status_code, 422, msg=response.content)
        self.assertFalse('access_token' in response.json())

    def test_wrong_username(self):
        with patch('whist_server.services.authentication.check_credentials',
                   side_effect=UserNotFoundError()):
            response = self.client.post(url='/user/auth',
                                        json={'username': 'miles', 'password': 'abcd'})
        self.assertEqual(response.status_code, 403, msg=response.content)
        self.assertFalse('access_token' in response.json())
