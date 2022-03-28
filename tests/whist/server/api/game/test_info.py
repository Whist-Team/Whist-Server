from unittest.mock import MagicMock

from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase
from whist.server.services.error import GameNotFoundError


class GameInfoTestCase(BaseCreateGameTestCase):
    def test_game_name_to_id(self):
        self.game_service_mock.get_by_name = MagicMock(return_value=self.game_mock)
        game_name: str = 'albatros'
        response = self.client.get(f'/game/info/id/{game_name}')
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('1', response.json()['id'])

    def test_game_name_to_id_not_found(self):
        self.game_service_mock.get_by_name = MagicMock(side_effect=GameNotFoundError())
        game_name: str = 'hornblower'
        response = self.client.get(f'/game/info/id/{game_name}')
        self.assertEqual(400, response.status_code, msg=response.content)
