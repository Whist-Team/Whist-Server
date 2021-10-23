import unittest

from starlette.testclient import TestClient

from whist.server import app
from whist.server.database import db


class TestCaseWithToken(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.login_creds = {'username': 'marcel', 'password': 'abc'}
        _ = self.client.post(url='/user/create', json=self.login_creds)
        token = self.client.post(url='/user/auth/', data=self.login_creds).json()['token']
        self.headers = {'Authorization': f'Bearer {token}'}

    def tearDown(self) -> None:
        db.game.drop()
        db.user.drop()
