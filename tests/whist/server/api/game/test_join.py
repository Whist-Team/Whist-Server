from tests.whist.server.api.game.base_token_case import TestCaseWithToken


class JoinGameTestCase(TestCaseWithToken):
    def setUp(self) -> None:
        super().setUp()
        self.game_creds = {'game_name': 'test', 'password': 'abc'}
        response = self.client.post(url='/game/create', json=self.game_creds, headers=self.headers)
        self.game_id = response.json()['game_id']

    def test_join(self):
        response = self.client.post(url=f'/game/join/{self.game_id}', json=self.game_creds,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertEqual('joined', response.json()['status'])
