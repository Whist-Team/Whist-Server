from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase


class JoinGameTestCase(BaseCreateGameTestCase):

    def test_join(self):
        headers = self.create_and_auth_user('miles', 'abc')
        response = self.client.post(url=f'/game/join/{self.game_id}',
                                    json={'password': 'abc'},
                                    headers=headers)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('joined', response.json()['status'])

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
