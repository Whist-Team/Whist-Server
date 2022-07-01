from threading import Thread
from time import sleep
from unittest import TestCase
from unittest.mock import patch, PropertyMock

import pytest
from starlette.testclient import TestClient
from whist.core.cards.card_container import UnorderedCardContainer

from whist.server import app
from whist.server.database import db
from whist.server.web_socket.events.event import PlayerJoinedEvent, CardPlayedEvent, \
    RoomStartedEvent, TrickDoneEvent


class NotificationTestCase(TestCase):
    """
    Integration Test Case
    """

    @classmethod
    def setUpClass(cls) -> None:
        db.user.drop()
        db.room.drop()
        cls.client = TestClient(app)
        cls.token = cls.create_and_auth_user('ws_user', '123')
        cls.headers = cls.create_and_auth_user('miles', 'abc')

    @classmethod
    def create_and_auth_user(cls, user: str, password):
        login_creds = {'username': user, 'password': password}
        _ = cls.client.post(url='/user/create', json=login_creds)
        token = cls.client.post(url='/user/auth', data=login_creds).json()['access_token']
        return {'Authorization': f'Bearer {token}'}

    def setUp(self) -> None:
        db.room.drop()
        data = {'room_name': 'test', 'password': 'abc', 'min_player': 1}
        response = self.client.post(url='/room/create', json=data, headers=self.token)
        self.room_id = response.json()['room_id']

    def tearDown(self) -> None:
        db.room.drop()

    @pytest.mark.integtest
    def test_join_notification(self):
        def call_noti(results):
            notification = websocket.receive_json()
            results.append(notification)

        def call_post():
            self.client.post(url=f'/room/join/{self.room_id}',
                             json={'password': 'abc'},
                             headers=self.headers)

        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(self.token['Authorization'].rsplit('Bearer ')[1])
            assert '200' == websocket.receive_text()
            notification = []
            thread_not = Thread(target=call_noti, args=[notification])
            thread_not.start()
            while not thread_not.is_alive():
                sleep(0.1)
            call_post()
            thread_not.join(30)
            self.assertFalse(thread_not.is_alive(), msg='Thread should been done by now')
            event = PlayerJoinedEvent(**notification[0]['event'])
            self.assertIsInstance(event, PlayerJoinedEvent)

    @pytest.mark.integtest
    def test_join_notification_no_game(self):
        with self.client.websocket_connect('/room/' + '1' * 24) as websocket:
            websocket.send_text(self.token['Authorization'].rsplit('Bearer ')[1])
            response = websocket.receive()
            self.assertEqual('Room not found', response['reason'])

    @pytest.mark.integtest
    def test_join_notification_not_joined(self):
        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            headers = self.create_and_auth_user('nico', 'abc')
            websocket.send_text(headers['Authorization'].rsplit('Bearer ')[1])
            response = websocket.receive()
            self.assertEqual('User not joined', response['reason'])

    @pytest.mark.integtest
    def test_start_notification(self):
        def call_noti(results):
            _ = websocket.receive_json()  # player joined
            notification = websocket.receive_json()
            results.append(notification)

        def call_post():
            self.client.post(url=f'/room/join/{self.room_id}',
                             json={'password': 'abc'},
                             headers=self.headers)
            self.client.post(url=f'/room/action/ready/{self.room_id}',
                             headers=self.headers)
            self.client.post(url=f'/room/action/ready/{self.room_id}',
                             headers=self.token)
            self.client.post(url=f'/room/action/start/{self.room_id}', headers=self.token,
                             json={'matcher_type': 'robin'})

        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(self.token['Authorization'].rsplit('Bearer ')[1])
            assert '200' == websocket.receive_text()
            notification = []
            thread_not = Thread(target=call_noti, args=[notification])
            thread_not.start()
            while not thread_not.is_alive():
                sleep(0.1)
            call_post()
            thread_not.join(30)
            self.assertFalse(thread_not.is_alive(), msg='Thread should been done by now')
            event = RoomStartedEvent(**notification[0]['event'])
            self.assertIsInstance(event, RoomStartedEvent)

    @pytest.mark.integtest
    def test_play_card_notification(self):
        def call_noti(results):
            _ = websocket.receive_json()  # player joined
            _ = websocket.receive_json()  # room started
            notification = websocket.receive_json()
            results.append(notification)

        def call_post():
            self.client.post(url=f'/room/join/{self.room_id}',
                             json={'password': 'abc'},
                             headers=self.headers)
            self.client.post(url=f'/room/action/ready/{self.room_id}',
                             headers=self.headers)
            self.client.post(url=f'/room/action/ready/{self.room_id}',
                             headers=self.token)
            self.client.post(url=f'/room/action/start/{self.room_id}', headers=self.token,
                             json={'matcher_type': 'robin'})

            response = self.client.get(url=f'/room/trick/hand/{self.room_id}',
                                       headers=self.token)
            hand = UnorderedCardContainer(**response.json())
            card = hand.cards[0]
            self.client.post(url=f'/room/trick/play_card/{self.room_id}',
                             json=card.dict(),
                             headers=self.token)

        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(self.token['Authorization'].rsplit('Bearer ')[1])
            assert '200' == websocket.receive_text()
            notification = []
            thread_not = Thread(target=call_noti, args=[notification])
            thread_not.start()
            while not thread_not.is_alive():
                sleep(0.1)
            call_post()
            thread_not.join(30)
            self.assertFalse(thread_not.is_alive(), msg='Thread should been done by now')
            event = CardPlayedEvent(**notification[0]['event'])
            self.assertIsInstance(event, CardPlayedEvent)

    @pytest.mark.integtest
    def test_last_play_card_notification(self):
        def call_noti(results):
            _ = websocket.receive_json()  # player joined
            _ = websocket.receive_json()  # game started
            card_played = websocket.receive_json()
            done_not = websocket.receive_json()
            results.append(card_played)
            results.append(done_not)

        def call_post():
            self.client.post(url=f'/game/join/{self.room_id}',
                             json={'password': 'abc'},
                             headers=self.headers)
            self.client.post(url=f'/game/action/ready/{self.room_id}',
                             headers=self.headers)
            self.client.post(url=f'/game/action/ready/{self.room_id}',
                             headers=self.token)
            self.client.post(url=f'/game/action/start/{self.room_id}', headers=self.token,
                             json={'matcher_type': 'robin'})

            response = self.client.get(url=f'/game/trick/hand/{self.room_id}',
                                       headers=self.token)
            hand = UnorderedCardContainer(**response.json())
            card = hand.cards[0]
            with patch('whist.core.game.trick.Trick.done', PropertyMock(return_value=True)):
                self.client.post(url=f'/game/trick/play_card/{self.room_id}',
                                 json=card.dict(),
                                 headers=self.token)

        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(self.token['Authorization'].rsplit('Bearer ')[1])
            assert '200' == websocket.receive_text()
            notification = []
            thread_not = Thread(target=call_noti, args=[notification])
            thread_not.start()
            while not thread_not.is_alive():
                sleep(0.1)
            call_post()
            thread_not.join(30)
            self.assertFalse(thread_not.is_alive(), msg='Thread should been done by now')
            event = CardPlayedEvent(**notification[0]['event'])
            self.assertIsInstance(event, CardPlayedEvent)
            event = TrickDoneEvent(**notification[1]['event'])
            self.assertIsInstance(event, TrickDoneEvent)
