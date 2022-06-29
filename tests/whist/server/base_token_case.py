import unittest
from unittest.mock import MagicMock

from starlette.testclient import TestClient
from whist.core.user.player import Player

from whist.server import app
from whist.server.database import db
from whist.server.services.authentication import get_current_user
from whist.server.services.channel_service import ChannelService
from whist.server.services.game_db_service import RoomDatabaseService
from whist.server.services.password import PasswordService
from whist.server.services.user_db_service import UserDatabaseService


class TestCaseWithToken(unittest.TestCase):
    def setUp(self) -> None:
        db.game.drop()
        db.user.drop()
        self.player_mock = Player(username='marcel', rating=2000)
        user_mock = MagicMock(name='user', to_user=self.player_mock)
        user_service = MagicMock(get=MagicMock(return_value=user_mock))
        self.game_service_mock = MagicMock(save=MagicMock(), add=MagicMock(return_value='1'))
        self.password_service_mock = MagicMock(verify=MagicMock())
        self.channel_service_mock = MagicMock()
        app.dependency_overrides[ChannelService] = lambda: self.channel_service_mock
        app.dependency_overrides[RoomDatabaseService] = lambda: self.game_service_mock
        app.dependency_overrides[PasswordService] = lambda: self.password_service_mock
        app.dependency_overrides[UserDatabaseService] = lambda: user_service
        app.dependency_overrides[get_current_user] = lambda: self.player_mock

        self.client = TestClient(app)
        self.app = app
        self.headers = self.create_and_auth_user('marcel', 'abc')

    def create_and_auth_user(self, user: str, password):
        login_creds = {'username': user, 'password': password}
        _ = self.client.post(url='/user/create', json=login_creds)
        token = self.client.post(url='/user/auth', data=login_creds).json()['access_token']
        return {'Authorization': f'Bearer {token}'}

    def tearDown(self) -> None:
        db.game.drop()
        db.user.drop()
