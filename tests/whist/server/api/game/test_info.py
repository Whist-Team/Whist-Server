from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase


class GameInfoTestCase(BaseCreateGameTestCase):
    def test_game_name_to_id(self):
        game_name: str = 'albatros'
        response = self.client.get(f'/game/info/id/{game_name}')
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('1', response.json()['id'])

    def test_game_name_to_id_not_found(self):
        game_name: str = 'hornblower'
        response = self.client.get(f'/game/info/id/{game_name}')
        self.assertEqual(400, response.status_code, msg=response.content)
