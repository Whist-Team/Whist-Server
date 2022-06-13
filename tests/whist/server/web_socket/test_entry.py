import asyncio

from tests.whist.server.base_token_case import TestCaseWithToken


async def print_response(websocket):
    print('wait for response')
    response = await websocket.receive_text
    print(response)


class EntryTestCase(TestCaseWithToken):
    def setUp(self) -> None:
        super().setUp()
        self.token = self.create_and_auth_user('simon', 'abc')
        data = {'game_name': 'test', 'password': 'abc'}
        response = self.client.post(url='/game/create', json=data, headers=self.headers)
        self.room_id = response.json()['game_id']

    def test_ping(self):
        with self.client.websocket_connect('/ping') as websocket:
            text = websocket.receive_text()
            self.assertEqual('pong', text)

    def test_subscribe(self):
        with self.client.websocket_connect('/room/{self.room_id}') as websocket:
            data = {'token': self.token}
            websocket.send_json(data)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(print_response(websocket))
