import unittest
from unittest.mock import MagicMock

from starlette.testclient import TestClient
from whist_core.user.player import Player

from whist_server import app
from whist_server.database import db
from whist_server.services.authentication import get_current_user
from whist_server.services.channel_service import ChannelService
from whist_server.services.password import PasswordService
from whist_server.services.room_db_service import RoomDatabaseService
from whist_server.services.user_db_service import UserDatabaseService


class TestCaseWithToken(unittest.TestCase):
    def setUp(self) -> None:
        db.room.drop()
        db.user.drop()
        self.player_mock = Player(username='marcel', rating=2000)
        user_mock = MagicMock(name='user', to_user=self.player_mock)
        user_service = MagicMock(get=MagicMock(return_value=user_mock))
        self.room_service_mock = MagicMock(save=MagicMock(), add=MagicMock(return_value='1'))
        self.password_service_mock = MagicMock(verify=MagicMock())
        self.channel_service_mock = MagicMock()
        app.dependency_overrides[ChannelService] = lambda: self.channel_service_mock
        app.dependency_overrides[RoomDatabaseService] = lambda: self.room_service_mock
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
        db.room.drop()
        db.user.drop()