from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase


class ActionGameTestCase(BaseCreateGameTestCase):
    def test_start(self):
        _ = self.client.post(url=f'/game/join/{self.game_id}',
                             json={'password': 'abcd'},
                             headers=self.headers)
        response = self.client.post(url=f'/game/action/start/{self.game_id}',
                                    headers=self.headers)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('started', response.json()['status'])

    def test_start_not_joined(self):
        response = self.client.post(url=f'/game/action/start/{self.game_id}',
                                    headers=self.headers)
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_ready(self):
        _ = self.client.post(url=f'/game/join/{self.game_id}',
                             json={'password': 'abcd'},
                             headers=self.headers)
        response = self.client.post(url=f'/game/action/ready/{self.game_id}',
                                    headers=self.headers)
        self.assertEqual(200, response.status_code, msg=response.content)

    def test_ready_not_joined(self):
        headers = self.create_and_auth_user('miles', 'abc')
        response = self.client.post(url=f'/game/action/ready/{self.game_id}',
                                    headers=headers)
        self.assertEqual(403, response.status_code, msg=response.content)
