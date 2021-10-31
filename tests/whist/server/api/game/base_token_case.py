import unittest

from starlette.testclient import TestClient

from whist.server import app
from whist.server.database import db


class TestCaseWithToken(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.headers = self.create_and_auth_user('marcel', 'abc')

    def create_and_auth_user(self, user: str, password):
        login_creds = {'username': user, 'password': password}
        _ = self.client.post(url='/user/create', json=login_creds)
        token = self.client.post(url='/user/auth/', data=login_creds).json()['token']
        return {'Authorization': f'Bearer {token}'}

    def tearDown(self) -> None:
        db.game.drop()
        db.user.drop()
