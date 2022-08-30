from unittest.mock import MagicMock

from tests.whist_server.api.game.base_created_case import BaseCreateGameTestCase


class GameTestCase(BaseCreateGameTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.hand_mock = MagicMock()
        self.room_mock.next_hand = MagicMock(return_value=self.hand_mock)

    def test_next_hand_success(self):
        response = self.client.post(url=f'/room/next_hand/{self.room_mock.id}')
        self.assertEqual('Success', response.json()['status'])
