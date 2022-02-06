import unittest
from unittest.mock import MagicMock

from starlette.testclient import TestClient

from whist.server import app
from whist.server.database import db
from whist.server.services.game_db_service import GameDatabaseService


class TestCaseWithToken(unittest.TestCase):
    def setUp(self) -> None:
        self.game_service_mock = MagicMock(save=MagicMock())
        app.dependency_overrides[GameDatabaseService] = lambda: self.game_service_mock

        self.client = TestClient(app)
        self.app = app
        self.headers = self.create_and_auth_user('marcel', 'abc')

    def create_and_auth_user(self, user: str, password):
        login_creds = {'username': user, 'password': password}
        _ = self.client.post(url='/user/create', json=login_creds)
        token = self.client.post(url='/user/auth/', data=login_creds).json()['token']
        return {'Authorization': f'Bearer {token}'}

    def tearDown(self) -> None:
        db.game.drop()
        db.user.drop()
