from unittest.mock import MagicMock

from tests.whist_server.api.game.base_created_case import BaseCreateGameTestCase

from whist_server.database.room import RoomInfo
from whist_server.services.error import RoomNotFoundError


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

    def test_get_room_info(self):
        expected_info = RoomInfo(name='test', password=True, rubber_number=0,
                                 game_number=0, hand_number=0, trick_number=0, min_player=2,
                                 max_player=2, player_number=1)
        self.room_mock.get_info = MagicMock(return_value=expected_info)
        self.room_service_mock.get = MagicMock(return_value=self.room_mock)
        response = self.client.get(f'/room/info/{self.room_mock.id}')
        room_info = RoomInfo(**response.json())

        self.assertEqual(expected_info, room_info)

    def test_get_room_info_not_found(self):
        self.room_service_mock.get = MagicMock(side_effect=RoomNotFoundError(
            game_id=self.room_mock.id))
        response = self.client.get(f'/room/info/{self.room_mock.id}')
        self.assertEqual(400, response.status_code, msg=response.content)
