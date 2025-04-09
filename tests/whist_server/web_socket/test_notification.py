from unittest import TestCase
from unittest.mock import patch, PropertyMock

import pytest
from starlette.testclient import TestClient
from whist_core.cards.card_container import UnorderedCardContainer

from whist_server import app
from whist_server.database import db
from whist_server.web_socket.events.event import PlayerJoinedEvent, CardPlayedEvent, \
    RoomStartedEvent, TrickDoneEvent


class NotificationTestCase(TestCase):
    """
    Integration Test Case
    """

    def create_and_auth_user(self, user: str, password: str):
        login_creds = {'username': user, 'password': password}
        _ = self.client.post(url='/user/create', json=login_creds).raise_for_status()
        token = self.client.post(url='/user/auth', data=login_creds).raise_for_status().json()['access_token']
        return {'Authorization': f'Bearer {token}'}

    def setUp(self):
        db.user.drop()
        db.room.drop()
        self.client = TestClient(app)
        self.headers_user1 = self.create_and_auth_user('ws_user', '123')
        self.headers_user2 = self.create_and_auth_user('user2', 'abc')
        data = {'room_name': 'test', 'password': 'abc', 'min_player': 1}
        response = self.client.post(url='/room/create', json=data, headers=self.headers_user1).raise_for_status()
        self.room_id = response.json()['room_id']

    def tearDown(self):
        db.room.drop()

    @pytest.mark.integtest
    def test_join_notification(self):
        def call_post():
            self.client.post(url=f'/room/join/{self.room_id}',
                             json={'password': 'abc'},
                             headers=self.headers_user2)

        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(self.headers_user1['Authorization'].rsplit('Bearer ')[1])
            assert '200' == websocket.receive_text()
            call_post()
            notification = websocket.receive_json()
            event = PlayerJoinedEvent(**notification['event'])
            self.assertIsInstance(event, PlayerJoinedEvent)

    @pytest.mark.skip(reason="broken")
    @pytest.mark.integtest
    def test_join_notification_no_game(self):
        with self.client.websocket_connect('/room/' + '1' * 24) as websocket:
            websocket.send_text(self.headers_user1['Authorization'].rsplit('Bearer ')[1])
            response = websocket.receive()
            self.assertEqual('Room not found', response['reason'])

    @pytest.mark.skip(reason="broken")
    @pytest.mark.integtest
    def test_join_notification_not_joined(self):
        headers = self.create_and_auth_user('nico', 'abc')
        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(headers['Authorization'].rsplit('Bearer ')[1])
            response = websocket.receive()
            self.assertEqual('User not joined', response['reason'])

    @pytest.mark.integtest
    def test_start_notification(self):
        def call_post():
            self.client.post(url=f'/room/join/{self.room_id}',
                             json={'password': 'abc'},
                             headers=self.headers_user2)
            self.client.post(url=f'/room/action/ready/{self.room_id}',
                             headers=self.headers_user2)
            self.client.post(url=f'/room/action/ready/{self.room_id}',
                             headers=self.headers_user1)
            self.client.post(url=f'/room/action/start/{self.room_id}', headers=self.headers_user1,
                             json={'matcher_type': 'robin'})

        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(self.headers_user1['Authorization'].rsplit('Bearer ')[1])
            assert '200' == websocket.receive_text()
            call_post()
            _ = websocket.receive_json()  # player joined
            notification = websocket.receive_json()
            event = RoomStartedEvent(**notification['event'])
            self.assertIsInstance(event, RoomStartedEvent)

    @pytest.mark.integtest
    def test_play_card_notification(self):
        def call_post():
            self.client.post(url=f'/room/join/{self.room_id}',
                             json={'password': 'abc'},
                             headers=self.headers_user2)
            self.client.post(url=f'/room/action/ready/{self.room_id}',
                             headers=self.headers_user2)
            self.client.post(url=f'/room/action/ready/{self.room_id}',
                             headers=self.headers_user1)
            self.client.post(url=f'/room/action/start/{self.room_id}', headers=self.headers_user1,
                             json={'matcher_type': 'robin'})

            response = self.client.get(url=f'/room/trick/hand/{self.room_id}',
                                       headers=self.headers_user1)
            hand = UnorderedCardContainer(**response.json())
            card = hand.cards[0]
            self.client.post(url=f'/room/trick/play_card/{self.room_id}',
                             json=card.model_dump(mode='json'),
                             headers=self.headers_user1)

        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(self.headers_user1['Authorization'].rsplit('Bearer ')[1])
            assert '200' == websocket.receive_text()
            call_post()
            _ = websocket.receive_json()  # player joined
            _ = websocket.receive_json()  # room started
            notification = websocket.receive_json()
            event = CardPlayedEvent(**notification['event'])
            self.assertIsInstance(event, CardPlayedEvent)

    @pytest.mark.integtest
    def test_last_play_card_notification(self):
        def call_post():
            self.client.post(url=f'/room/join/{self.room_id}',
                             json={'password': 'abc'},
                             headers=self.headers_user2)
            self.client.post(url=f'/room/action/ready/{self.room_id}',
                             headers=self.headers_user2)
            self.client.post(url=f'/room/action/ready/{self.room_id}',
                             headers=self.headers_user1)
            self.client.post(url=f'/room/action/start/{self.room_id}', headers=self.headers_user1,
                             json={'matcher_type': 'robin'})

            response = self.client.get(url=f'/room/trick/hand/{self.room_id}',
                                       headers=self.headers_user1)
            hand = UnorderedCardContainer(**response.json())
            card = hand.cards[0]
            with patch('whist_core.game.trick.Trick.done', PropertyMock(return_value=True)):
                self.client.post(url=f'/room/trick/play_card/{self.room_id}',
                                 json=card.model_dump(),
                                 headers=self.headers_user1)

        with self.client.websocket_connect(f'/room/{self.room_id}') as websocket:
            websocket.send_text(self.headers_user1['Authorization'].rsplit('Bearer ')[1])
            assert '200' == websocket.receive_text()
            call_post()
            _ = websocket.receive_json()  # player joined
            _ = websocket.receive_json()  # room started
            card_played = websocket.receive_json()
            event = CardPlayedEvent(**card_played['event'])
            self.assertIsInstance(event, CardPlayedEvent)
            done_not = websocket.receive_json()
            event = TrickDoneEvent(**done_not['event'])
            self.assertIsInstance(event, TrickDoneEvent)
