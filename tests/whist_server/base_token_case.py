import unittest
from unittest.mock import MagicMock

from starlette.testclient import TestClient
from whist_core.user.player import Player

from whist_server import app
from whist_server.services.authentication import get_current_user
from whist_server.services.channel_service import ChannelService
from whist_server.services.password import PasswordService
from whist_server.services.room_db_service import RoomDatabaseService
from whist_server.services.splunk_service import SplunkService
from whist_server.services.user_db_service import UserDatabaseService


class TestCaseWithToken(unittest.TestCase):
    def setUp(self) -> None:
        self.player_mock = Player(username='marcel', rating=2000)
        user_mock = MagicMock(name='user', to_player=self.player_mock)
        self.user_service_mock = MagicMock(get=MagicMock(return_value=user_mock))
        self.room_service_mock = MagicMock(save=MagicMock(), add=MagicMock(return_value='1'))
        self.password_service_mock = MagicMock(verify=MagicMock(),
                                               hash=MagicMock(return_value='1' * 12))
        self.channel_service_mock = MagicMock()
        self.splunk_service_mock = MagicMock()
        app.dependency_overrides[ChannelService] = lambda: self.channel_service_mock
        app.dependency_overrides[RoomDatabaseService] = lambda: self.room_service_mock
        app.dependency_overrides[PasswordService] = lambda: self.password_service_mock
        app.dependency_overrides[UserDatabaseService] = lambda: self.user_service_mock
        app.dependency_overrides[get_current_user] = lambda: self.player_mock
        app.dependency_overrides[SplunkService] = lambda: self.splunk_service_mock

        self.client = TestClient(app)
        self.app = app
        self.headers = self.create_and_auth_user()

    def create_and_auth_user(self):
        token = '1' * 24
        return {'Authorization': f'Bearer {token}'}
