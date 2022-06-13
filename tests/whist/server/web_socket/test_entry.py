from unittest.mock import MagicMock

from tests.whist.server.base_token_case import TestCaseWithToken
from whist.server import app
from whist.server.services.error import GameNotFoundError
from whist.server.services.game_db_service import GameDatabaseService


class EntryTestCase(TestCaseWithToken):
    def setUp(self) -> None:
        super().setUp()
        self.token = self.create_and_auth_user('simon', 'abc')
        data = {'game_name': 'test', 'password': 'abc'}
        response = self.client.post(url='/game/create', json=data, headers=self.headers)
        self.room_id = response.json()['game_id']
        channel_mock = MagicMock()
        self.game_mock = MagicMock(side_channel=channel_mock)

    def test_ping(self):
        with self.client.websocket_connect('/ping') as websocket:
            text = websocket.receive_text()
            self.assertEqual('pong', text)

    def test_subscribe(self):
        self.game_service_mock.get = MagicMock(return_value=self.game_mock)
        app.dependency_overrides[GameDatabaseService] = lambda: self.game_service_mock
        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            data = {'token': self.token}
            websocket.send_json(data)
            response = websocket.receive_text()
            self.game_mock.side_channel.attach.assert_called_once()
            self.assertEqual('200', response)

    def test_subscribe_room_not_exists(self):
        self.game_service_mock.get = MagicMock(side_effect=GameNotFoundError)
        app.dependency_overrides[GameDatabaseService] = lambda: self.game_service_mock
        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            data = {'token': self.token}
            websocket.send_json(data)
            response = websocket.receive_text()
            self.game_mock.side_channel.attach.assert_not_called()
            self.assertEqual('Game not found', response)
