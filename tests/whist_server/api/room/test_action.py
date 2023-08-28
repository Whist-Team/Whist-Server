from unittest.mock import MagicMock

from whist_core.error.table_error import TableNotReadyError, PlayerNotJoinedError

from tests.whist_server.api.room.base_created_case import BaseCreateGameTestCase
from whist_server.database.error import PlayerNotCreatorError
from whist_server.services.error import RoomNotFoundError
from whist_server.services.error import UserNotReadyError
from whist_server.services.room_db_service import RoomDatabaseService


class ActionGameTestCase(BaseCreateGameTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.second_player = self.create_and_auth_user()
        self.game_service = RoomDatabaseService()

    def test_start(self):
        # Request to start table.
        response = self.client.post(url=f'/room/action/start/{self.room_mock.id}',
                                    headers=self.headers,
                                    json={'matcher_type': 'robin'})
        self.room_mock.start.assert_called_once()
        self.room_service_mock.save.assert_called_once_with(self.room_mock)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('started', response.json()['status'])

    def test_start_not_creator(self):
        self.room_mock.start = MagicMock(side_effect=PlayerNotCreatorError)

        # New user tries to start table.
        response = self.client.post(url=f'/room/action/start/{self.room_mock.id}',
                                    headers=self.second_player,
                                    json={'matcher_type': 'robin'})
        self.room_mock.start.assert_called_once()
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_start_no_room(self):
        self.room_service_mock.get = MagicMock(side_effect=RoomNotFoundError('999'))
        response = self.client.post(url='/room/action/start/999', headers=self.headers,
                                    json={'matcher_type': 'robin'})
        self.room_mock.assert_not_called()
        self.assertEqual(404, response.status_code, msg=response.content)

    def test_start_table_not_ready(self):
        self.room_mock.start = MagicMock(side_effect=TableNotReadyError)
        # Request to start table.
        response = self.client.post(url=f'/room/action/start/{self.room_mock.id}',
                                    headers=self.headers,
                                    json={'matcher_type': 'robin'})
        self.room_mock.start.assert_called_once()
        self.assertEqual(400, response.status_code, msg=response.content)

    def test_ready(self):
        response = self.client.post(url=f'/room/action/ready/{self.room_mock.id}',
                                    headers=self.headers)
        self.room_mock.ready_player.assert_called_once()
        self.assertEqual(200, response.status_code, msg=response.content)

    def test_ready_not_joined(self):
        self.room_mock.ready_player = MagicMock(side_effect=PlayerNotJoinedError)
        response = self.client.post(url=f'/room/action/ready/{self.room_mock.id}',
                                    headers=self.second_player)
        self.room_mock.ready_player.assert_called_once()
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_ready_no_room(self):
        self.room_service_mock.get = MagicMock(side_effect=RoomNotFoundError('999'))
        response = self.client.post(url='/room/action/ready/999', headers=self.headers)
        self.room_mock.assert_not_called()
        self.assertEqual(404, response.status_code, msg=response.content)

    def test_unready(self):
        response = self.client.post(url=f'/room/action/unready/{self.room_mock.id}',
                                    headers=self.headers)
        self.room_mock.unready_player.assert_called_once()
        self.assertEqual(200, response.status_code, msg=response.content)

    def test_unready_not_joined(self):
        self.room_mock.unready_player = MagicMock(side_effect=PlayerNotJoinedError)
        response = self.client.post(url=f'/room/action/unready/{self.room_mock.id}',
                                    headers=self.second_player)
        self.room_mock.unready_player.assert_called_once()
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_unready_player_not_ready(self):
        self.room_mock.unready_player = MagicMock(side_effect=UserNotReadyError)
        response = self.client.post(url=f'/room/action/unready/{self.room_mock.id}',
                                    headers=self.second_player)
        self.room_mock.unready_player.assert_called_once()
        self.assertEqual(400, response.status_code, msg=response.content)

    def test_unready_no_room(self):
        self.room_service_mock.get = MagicMock(side_effect=RoomNotFoundError('998'))
        response = self.client.post(url='/room/action/unready/998', headers=self.headers)
        self.room_mock.assert_not_called()
        self.assertEqual(404, response.status_code, msg=response.content)

    def test_unready_no_room_save(self):
        self.room_service_mock.save = MagicMock(side_effect=RoomNotFoundError('999'))
        response = self.client.post(url='/room/action/unready/999', headers=self.headers)
        self.room_mock.assert_not_called()
        self.assertEqual(404, response.status_code, msg=response.content)
