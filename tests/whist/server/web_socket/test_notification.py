import json
from threading import Thread
from time import sleep
from unittest import TestCase

import pytest
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from whist.core.cards.card_container import UnorderedCardContainer

from whist.server import app
from whist.server.database import db
from whist.server.web_socket.events.event import PlayerJoinedEvent, CardPlayedEvent


class NotificationTestCase(TestCase):
    """
    Integration Test Case
    """

    @classmethod
    def setUpClass(cls) -> None:
        db.user.drop()
        cls.client = TestClient(app)
        cls.token = cls.create_and_auth_user('ws_user', '123')

    @classmethod
    def create_and_auth_user(cls, user: str, password):
        login_creds = {'username': user, 'password': password}
        _ = cls.client.post(url='/user/create', json=login_creds)
        token = cls.client.post(url='/user/auth', data=login_creds).json()['access_token']
        return {'Authorization': f'Bearer {token}'}

    def setUp(self) -> None:
        db.game.drop()
        data = {'game_name': 'test', 'password': 'abc', 'min_player': 1}
        response = self.client.post(url='/game/create', json=data, headers=self.token)
        self.room_id = response.json()['game_id']

    def tearDown(self) -> None:
        db.game.drop()

    @pytest.mark.integtest
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
            thread_not.start()
            while not thread_not.is_alive():
                sleep(0.1)
            call_post()
            thread_not.join(30)
            self.assertFalse(thread_not.is_alive(), msg='Thread should been done by now')
            event = PlayerJoinedEvent(**json.loads(notification[0]['event']))
            self.assertIsInstance(event, PlayerJoinedEvent)

    @pytest.mark.integtest
    def test_join_notification_no_game(self):
        with self.assertRaises(WebSocketDisconnect):
            with self.client.websocket_connect('/room/' + '1' * 24):
                pass

    @pytest.mark.integtest
    def test_play_card_notification(self):
        def call_noti(results):
            _ = websocket.receive_json()  # player joined
            notification = websocket.receive_json()
            results.append(notification)

        def call_post():
            self.client.post(url=f'/game/join/{self.room_id}',
                             json={'password': 'abc'},
                             headers=headers)
            self.client.post(url=f'/game/action/ready/{self.room_id}',
                             headers=headers)
            self.client.post(url=f'/game/action/ready/{self.room_id}',
                             headers=self.token)
            self.client.post(url=f'/game/action/start/{self.room_id}', headers=self.token,
                             json={'matcher_type': 'robin'})

            response = self.client.get(url=f'/game/trick/hand/{self.room_id}',
                                       headers=self.token)
            hand = UnorderedCardContainer(**response.json())
            card = hand.cards[0]
            response = self.client.post(url=f'/game/trick/play_card/{self.room_id}',
                                        json=card.dict(),
                                        headers=self.token)
            response

        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(self.token['Authorization'].rsplit('Bearer ')[1])
            assert '200' == websocket.receive_text()
            headers = self.create_and_auth_user('miles', 'abc')
            notification = []
            thread_not = Thread(target=call_noti, args=[notification])
            thread_not.start()
            while not thread_not.is_alive():
                sleep(0.1)
            call_post()
            thread_not.join(30)
            self.assertFalse(thread_not.is_alive(), msg='Thread should been done by now')
            event = CardPlayedEvent(**json.loads(notification[0]['event']))
            self.assertIsInstance(event, CardPlayedEvent)
