from tests.whist.server.base_token_case import TestCaseWithToken


class EntryTestCase(TestCaseWithToken):
    def setUp(self) -> None:
        super().setUp()
        self.token = self.create_and_auth_user('simon', 'abc')
        data = {'game_name': 'test', 'password': 'abc'}
        response = self.client.post(url='/game/create', json=data, headers=self.headers)
        self.room_id = response.json()['game_id']

    def test_subscribe(self):
        with self.client.websocket_connect('/room/{self.room_id}') as websocket:
            data = {'token': self.token}
            websocket.send_json(data)
