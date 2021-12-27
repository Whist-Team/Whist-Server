from tests.whist.server.api.game.base_token_case import TestCaseWithToken

class BaseCreateGameTestCase(TestCaseWithToken):
    def setUp(self) -> None:
        super().setUp()
        self.game_creds = {'game_name': 'test', 'password': 'abc'}
        response = self.client.post(url='/game/create', json=self.game_creds, headers=self.headers)
        self.game_id = response.json()['game_id']
