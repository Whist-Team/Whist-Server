from unittest.mock import MagicMock

from tests.whist_server.base_token_case import TestCaseWithToken
from whist_server.database.room import RoomInDb
from whist_server.services.password import PasswordService


class CreateGameTestCase(TestCaseWithToken):
    def setUp(self) -> None:
        super().setUp()
        self.prefix = 'room'
        self.game_in_db_mock = MagicMock(create_with_pwd=MagicMock())
        self.app.dependency_overrides[RoomInDb] = lambda: self.game_in_db_mock
        self.room_service_mock.add = MagicMock(return_value=1)
        self.app.dependency_overrides[PasswordService] = lambda: MagicMock(
            hash=MagicMock(return_value='abc'))

    def test_post_game(self):
        data = {'room_name': 'test', 'password': 'abc'}
        response = self.client.post(url=f'/{self.prefix}/create', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertEqual(1, response.json()['room_id'])
        self.room_service_mock.create_with_pwd.assert_called_once_with(room_name='test',
                                                                       hashed_password='abc',
                                                                       creator=self.player_mock,
                                                                       min_player=None,
                                                                       max_player=None)

    def test_post_game_without_pwd(self):
        data = {'room_name': 'test'}
        response = self.client.post(url=f'/{self.prefix}/create', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertEqual(1, response.json()['room_id'])
        self.room_service_mock.create_with_pwd.assert_called_once_with(room_name='test',
                                                                       hashed_password=None,
                                                                       creator=self.player_mock,
                                                                       min_player=None,
                                                                       max_player=None)

    def test_post_game_without_name(self):
        data = {'password': 'abc'}
        response = self.client.post(url=f'/{self.prefix}/create', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 422, msg=response.content)

    def test_post_game_with_settings(self):
        data = {'room_name': 'test', 'password': 'abc', 'min_player': 1, 'max_player': 1}
        response = self.client.post(url=f'/{self.prefix}/create', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertEqual(1, response.json()['room_id'])
        self.room_service_mock.create_with_pwd.assert_called_once_with(room_name='test',
                                                                       hashed_password='abc',
                                                                       creator=self.player_mock,
                                                                       min_player=1, max_player=1)
