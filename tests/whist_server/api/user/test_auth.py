import unittest

from starlette.testclient import TestClient

from whist_server import app
from whist_server.database import db


class AuthTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.login_creds = {'username': 'marcel', 'password': 'abc'}
        _ = self.client.post(url='/user/create', json=self.login_creds)

    def tearDown(self) -> None:
        db.user.drop()

    def test_auth_user(self):
        response = self.client.post(url='/user/auth', data=self.login_creds)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertTrue('access_token' in response.json())

    def test_wrong_password(self):
        response = self.client.post(url='/user/auth',
                                    data={'username': 'marcel', 'password': 'abcd'})
        self.assertEqual(response.status_code, 401, msg=response.content)
        self.assertFalse('access_token' in response.json())

    def test_no_password(self):
        response = self.client.post(url='/user/auth', data={'username': 'marcel'})
        self.assertEqual(response.status_code, 422, msg=response.content)
        self.assertFalse('access_token' in response.json())

    def test_no_username(self):
        response = self.client.post(url='/user/auth', data={'password': 'abc'})
        self.assertEqual(response.status_code, 422, msg=response.content)
        self.assertFalse('access_token' in response.json())

    def test_wrong_username(self):
        response = self.client.post(url='/user/auth',
                                    data={'username': 'miles', 'password': 'abcd'})
        self.assertEqual(response.status_code, 403, msg=response.content)
        self.assertFalse('access_token' in response.json())