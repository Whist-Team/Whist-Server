from unittest.mock import MagicMock

from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase
from whist.server.services.error import RoomNotFoundError


class GameInfoTestCase(BaseCreateGameTestCase):
    def test_game_name_to_id(self):
        self.room_service_mock.get_by_name = MagicMock(return_value=self.room_mock)
        game_name: str = 'albatros'
        response = self.client.get(f'/room/info/id/{game_name}')
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('1', response.json()['id'])

    def test_game_name_to_id_login_required(self):
        self.app.dependency_overrides = {}
        self.room_service_mock.get_by_name = MagicMock(return_value=self.room_mock)
        game_name: str = 'albatros'
        response = self.client.get(f'/room/info/id/{game_name}')
        self.assertEqual(401, response.status_code, msg=response.content)

    def test_game_name_to_id_not_joined(self):
        self.room_mock.has_joined = MagicMock(return_value=False)
        self.room_service_mock.get_by_name = MagicMock(return_value=self.room_mock)
        game_name: str = 'albatros'
        response = self.client.get(f'/room/info/id/{game_name}')
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_game_name_to_id_not_found(self):
        self.room_service_mock.get_by_name = MagicMock(side_effect=RoomNotFoundError())
        game_name: str = 'hornblower'
        response = self.client.get(f'/room/info/id/{game_name}')
        self.assertEqual(400, response.status_code, msg=response.content)

    def test_get_all_ids(self):
        self.room_service_mock.all = MagicMock(return_value=[self.room_mock])
        response = self.client.get('/room/info/ids')
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual(['1'], response.json()['rooms'])

    def test_get_all_ids_require_login(self):
        self.app.dependency_overrides = {}
        self.room_service_mock.all = MagicMock(return_value=[self.room_mock])
        response = self.client.get('/room/info/ids')
        self.assertEqual(401, response.status_code, msg=response.content)
