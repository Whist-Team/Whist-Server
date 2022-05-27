from unittest.mock import MagicMock

from whist.core.error.table_error import TableNotReadyError, PlayerNotJoinedError

from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase
from whist.server.database.error import PlayerNotCreatorError
from whist.server.services.game_db_service import GameDatabaseService


class PlayerNotReadyError(Exception):
    """
    Will check to see if player is ready before unreadying
    """


class GameNotFoundError(Exception):
    """
    Checks to see if user enters correct game_id
    """


class ActionGameTestCase(BaseCreateGameTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.second_player = self.create_and_auth_user('miles', 'abc')
        self.game_service = GameDatabaseService()

    def test_start(self):
        # Request to start table.
        response = self.client.post(url=f'/game/action/start/{self.game_mock.id}',
                                    headers=self.headers,
                                    json={'matcher_type': 'robin'})
        self.game_mock.start.assert_called_once()
        self.game_service_mock.save.assert_called_once_with(self.game_mock)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('started', response.json()['status'])

    def test_start_not_creator(self):
        self.game_mock.start = MagicMock(side_effect=PlayerNotCreatorError)

        # New user tries to start table.
        response = self.client.post(url=f'/game/action/start/{self.game_mock.id}',
                                    headers=self.second_player,
                                    json={'matcher_type': 'robin'})
        self.game_mock.start.assert_called_once()
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_start_table_not_ready(self):
        self.game_mock.start = MagicMock(side_effect=TableNotReadyError)
        # Request to start table.
        response = self.client.post(url=f'/game/action/start/{self.game_mock.id}',
                                    headers=self.headers,
                                    json={'matcher_type': 'robin'})
        self.game_mock.start.assert_called_once()
        self.assertEqual(400, response.status_code, msg=response.content)

    def test_ready(self):
        response = self.client.post(url=f'/game/action/ready/{self.game_mock.id}',
                                    headers=self.headers)
        self.game_mock.ready_player.assert_called_once()
        self.assertEqual(200, response.status_code, msg=response.content)

    def test_ready_not_joined(self):
        self.game_mock.ready_player = MagicMock(side_effect=PlayerNotJoinedError)
        response = self.client.post(url=f'/game/action/ready/{self.game_mock.id}',
                                    headers=self.second_player)
        self.game_mock.ready_player.assert_called_once()
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_unready(self):
        response = self.client.post(url=f'/game/action/unready/{self.game_mock.id}',
                                    headers=self.headers)
        self.game_mock.unready_player.assert_called_once()
        self.assertEqual(200, response.status_code, msg=response.content)

    def test_unready_game_not_found(self):
        self.game_mock.unready_player = MagicMock(side_effect=GameNotFoundError)
        response = self.client.post(url=f'/game/action/unready/{self.game_mock.id}',
                                    headers=self.second_player)
        self.game_mock.unready_player.assert_called_once()
        self.assertEqual(404, response.status_code, msg=response.content)

    def test_unready_not_joined(self):
        self.game_mock.unready_player = MagicMock(side_effect=PlayerNotJoinedError)
        response = self.client.post(url=f'/game/action/unready/{self.game_mock.id}',
                                    headers=self.second_player)
        self.game_mock.unready_player.assert_called_once()
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_unready_player_not_ready(self):
        self.game_mock.unready_player = MagicMock(side_effect=PlayerNotReadyError)
        response = self.client.post(url=f'/game/action/unready/{self.game_mock.id}',
                                    headers=self.second_player)
        self.game_mock.unready_player.assert_called_once()
        self.assertEqual(400, response.status_code, msg=response.content)
