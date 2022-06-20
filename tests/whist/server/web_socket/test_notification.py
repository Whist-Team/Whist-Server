import json
from threading import Thread
from time import sleep
from unittest import TestCase

from starlette.testclient import TestClient

from whist.server import app
from whist.server.web_socket.events.event import PlayerJoinedEvent


class NotificationTestCase(TestCase):
    """
    Integration Test Case
    """

    def create_and_auth_user(self, user: str, password):
        login_creds = {'username': user, 'password': password}
        _ = self.client.post(url='/user/create', json=login_creds)
        token = self.client.post(url='/user/auth/', data=login_creds).json()['token']
        return {'Authorization': f'Bearer {token}'}

    def setUp(self) -> None:
        self.client = TestClient(app)
        self.token = self.create_and_auth_user('ws_user', '123')
        data = {'game_name': 'test', 'password': 'abc'}
        response = self.client.post(url='/game/create', json=data, headers=self.token)
        self.room_id = response.json()['game_id']

    def test_join_notification(self):
        def call_noti(results):
            notification = websocket.receive_json()
            results.append(notification)

        def call_post():
            self.client.post(url=f'/game/join/{self.room_id}',
                             json={'password': 'abc'},
                             headers=headers)

        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(self.token['Authorization'].rsplit('Bearer ')[1])
            assert '200' == websocket.receive_text()
            headers = self.create_and_auth_user('miles', 'abc')
            notification = []
            thread_not = Thread(target=call_noti, args=[notification])
            thread_post = Thread(target=call_post)
            thread_not.start()
            thread_post.start()
            while thread_not.is_alive():
                sleep(0.1)
            event = PlayerJoinedEvent(**json.loads(notification[0]['event']))
            self.assertIsInstance(event, PlayerJoinedEvent)
