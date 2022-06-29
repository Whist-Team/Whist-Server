from unittest import skip
from unittest.mock import MagicMock

from tests.whist.server.base_token_case import TestCaseWithToken
from whist.server import app
from whist.server.services.channel_service import ChannelService
from whist.server.services.error import RoomNotFoundError
from whist.server.services.room_db_service import RoomDatabaseService


class EntryTestCase(TestCaseWithToken):
    def setUp(self) -> None:
        super().setUp()
        self.token = self.create_and_auth_user('simon', 'abc')['Authorization'].rsplit('Bearer ')[1]
        data = {'game_name': 'test', 'password': 'abc'}
        response = self.client.post(url='/game/create', json=data, headers=self.headers)
        self.room_id = response.json()['game_id']
        channel_mock = MagicMock()
        self.game_mock = MagicMock(side_channel=channel_mock)
        self.channel_service_mock = MagicMock()
        app.dependency_overrides[ChannelService] = lambda x: self.channel_service_mock

    def test_ping(self):
        with self.client.websocket_connect('/ping') as websocket:
            text = websocket.receive_text()
            self.assertEqual('pong', text)

    @skip('Probably bug in Test Client')
    def test_subscribe(self):
        self.game_mock.has_joined = MagicMock(return_value=True)
        self.game_service_mock.get = MagicMock(return_value=self.game_mock)
        app.dependency_overrides[RoomDatabaseService] = lambda: self.game_service_mock
        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(self.token)
            response = websocket.receive_text()
            self.channel_service_mock.attach.assert_called_once()
            self.assertEqual('200', response)

    @skip('Probably bug in Test Client')
    def test_subscribe_room_not_exists(self):
        self.game_service_mock.get = MagicMock(side_effect=RoomNotFoundError)
        app.dependency_overrides[RoomDatabaseService] = lambda: self.game_service_mock
        with self.client.websocket_connect(f'/room/{self.room_id}1') as websocket:
            websocket.send_text(self.token)
            response = websocket.receive_text()
            self.channel_service_mock.attach.assert_not_called()
            self.assertEqual('Game not found', response)

    @skip('Probably bug in Test Client')
    def test_subscribe_not_joined(self):
        self.game_mock.has_joined = MagicMock(return_value=False)
        self.game_service_mock.get = MagicMock(return_value=self.game_mock)
        app.dependency_overrides[RoomDatabaseService] = lambda: self.game_service_mock
        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(self.token)
            response = websocket.receive_text()
            self.channel_service_mock.attach.assert_not_called()
            self.assertEqual('User not joined', response)
