from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase
from whist.server.services.game_db_service import GameDatabaseService


class JoinGameTestCase(BaseCreateGameTestCase):

    def test_join(self):
        headers = self.create_and_auth_user('miles', 'abc')
        response = self.client.post(url=f'/game/join/{self.game_id}',
                                    json={'password': 'abc'},
                                    headers=headers)
        game_service = GameDatabaseService()
        db_game = game_service.get(self.game_id)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('joined', response.json()['status'])
        self.assertEqual(len(db_game.players), 2)

    def test_join_wrong_pwd_game(self):
        response = self.client.post(url=f'/game/join/{self.game_id}',
                                    json={'password': 'abcd'},
                                    headers=self.headers)
        self.assertEqual(401, response.status_code, msg=response.content)

    def test_host_join(self):
        response = self.client.post(url=f'/game/join/{self.game_id}',
                                    json={'password': 'abc'},
                                    headers=self.headers)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('already joined', response.json()['status'])
