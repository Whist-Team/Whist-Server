from unittest.mock import MagicMock

from whist_core.game.errors import HandNotDoneError

from tests.whist_server.api.room.base_created_case import BaseCreateGameTestCase
from whist_server import app


class GameTestCase(BaseCreateGameTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.hand_mock = MagicMock()
        self.room_mock.next_hand = MagicMock(return_value=self.hand_mock)
        self.room_mock.players = [self.player_mock]

    def test_next_hand_success(self):
        response = self.client.post(url=f'/room/next_hand/{self.room_mock.id}',
                                    headers=self.headers)
        self.room_mock.next_hand.assert_called_once()
        self.assertEqual('Success', response.json()['status'])
        self.assertEqual(200, response.status_code)

    def test_next_hand_without_user(self):
        app.dependency_overrides = {}
        response = self.client.post(url=f'/room/next_hand/{self.room_mock.id}')
        self.room_mock.next_hand.assert_not_called()
        self.assertEqual(401, response.status_code)

    def test_next_hand_user_not_joined(self):
        self.room_mock.players = []
        response = self.client.post(url=f'/room/next_hand/{self.room_mock.id}',
                                    headers=self.headers)
        self.room_mock.next_hand.assert_not_called()
        self.assertEqual(403, response.status_code)

    def test_next_hand_not_done(self):
        self.room_mock.next_hand = MagicMock(side_effect=HandNotDoneError())
        response = self.client.post(url=f'/room/next_hand/{self.room_mock.id}',
                                    headers=self.headers)
        self.room_mock.next_hand.assert_called_once()
        self.assertEqual(400, response.status_code)
