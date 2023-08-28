from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock

import pytest
from starlette.testclient import TestClient
from whist_core.cards.card import Card, Suit, Rank
from whist_core.cards.card_container import OrderedCardContainer

from tests.whist_server.api.room.base_created_case import BaseCreateGameTestCase
from whist_server import app
from whist_server.api.room.join import ReconnectArguments
from whist_server.database import db
from whist_server.database.error import PlayerNotJoinedError
from whist_server.database.room import RoomInfo
from whist_server.database.warning import PlayerAlreadyJoinedWarning
from whist_server.services.error import RoomNotFoundError


class JoinGameTestCase(BaseCreateGameTestCase):

    def test_join(self):
        headers = self.create_and_auth_user()
        self.password_service_mock.verify = MagicMock(return_value=True)

        response = self.client.post(url=f'/room/join/{self.room_mock.id}',
                                    json={'password': 'abc'},
                                    headers=headers)
        self.room_mock.join.assert_called_once()
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('joined', response.json()['status'])

    def test_join_wrong_pwd_game(self):
        self.password_service_mock.verify = MagicMock(return_value=False)
        response = self.client.post(url=f'/room/join/{self.room_mock.id}',
                                    json={'password': 'abcd'},
                                    headers=self.headers)
        self.assertEqual(401, response.status_code, msg=response.content)

    def test_join_login_required(self):
        self.app.dependency_overrides = {}
        self.password_service_mock.verify = MagicMock(return_value=True)
        response = self.client.post(url=f'/room/join/{self.room_mock.id}',
                                    json={'password': 'abc'})
        self.assertEqual(401, response.status_code, msg=response.content)

    def test_reconnect(self):
        self.room_mock.has_password = True
        self.room_mock.table.started = True
        room_info = RoomInfo.from_room(self.room_mock)
        self.room_service_mock.get_by_user_id = MagicMock(return_value=self.room_mock)
        response = self.client.post(url='/room/reconnect/',
                                    headers=self.headers)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('joined', response.json()['status'])
        self.assertEqual(room_info, RoomInfo(**response.json()['room_info']))
        self.assertEqual(self.room_mock.id, response.json()['room_id'])

    def test_reconnect_with_stack(self):
        self.room_mock.has_password = True
        self.room_mock.table.started = True
        expected_stack = OrderedCardContainer.with_cards((Card(rank=Rank.A, suit=Suit.CLUBS)))
        self.room_mock.current_trick = MagicMock(return_value=PropertyMock(stack=expected_stack))
        room_info = RoomInfo.from_room(self.room_mock)
        self.room_service_mock.get_by_user_id = MagicMock(return_value=self.room_mock)
        response = self.client.post(url='/room/reconnect/', headers=self.headers,
                                    json=ReconnectArguments(stack=True).dict())
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('joined', response.json()['status'])
        self.assertEqual(room_info, RoomInfo(**response.json()['room_info']))
        self.assertEqual(self.room_mock.id, response.json()['room_id'])
        self.assertEqual(expected_stack, OrderedCardContainer(**response.json()['stack']))

    def test_reconnect_not_joined(self):
        self.room_mock.has_password = True
        self.room_service_mock.get_by_user_id = MagicMock(side_effect=RoomNotFoundError())
        response = self.client.post(url='/room/reconnect/',
                                    headers=self.headers)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('not joined', response.json()['status'])
        self.assertNotIn('room_info', response.json().keys())
        self.assertNotIn('room_id', response.json().keys())

    def test_host_join(self):
        self.room_mock.join = MagicMock(side_effect=PlayerAlreadyJoinedWarning)
        response = self.client.post(url=f'/room/join/{self.room_mock.id}',
                                    json={'password': 'abc'},
                                    headers=self.headers)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('already joined', response.json()['status'])

    def test_join_no_room(self):
        self.room_service_mock.get = MagicMock(side_effect=RoomNotFoundError('999'))
        response = self.client.post(url='/room/join/999', json={'password': 'abc'},
                                    headers=self.headers)
        self.room_mock.assert_not_called()
        self.assertEqual(404, response.status_code, msg=response.content)

    def test_leave(self):
        headers = self.create_and_auth_user()
        self.password_service_mock.verify = MagicMock(return_value=True)

        response = self.client.post(url=f'/room/leave/{self.room_mock.id}',
                                    headers=headers)
        self.room_mock.leave.assert_called_once()
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('left', response.json()['status'])

    def test_leave_not_joined(self):
        headers = self.create_and_auth_user()
        self.password_service_mock.verify = MagicMock(return_value=True)
        self.room_mock.leave = MagicMock(side_effect=PlayerNotJoinedError)
        response = self.client.post(url=f'/room/leave/{self.room_mock.id}',
                                    headers=headers)
        self.room_mock.leave.assert_called_once()
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_leave_no_room(self):
        self.room_service_mock.get = MagicMock(side_effect=RoomNotFoundError('999'))
        response = self.client.post(url='/room/leave/999', headers=self.headers)
        self.room_mock.assert_not_called()
        self.assertEqual(404, response.status_code, msg=response.content)


class IntegrationTestJoinGame(TestCase):
    def create_and_auth_user(self, user: str, password):
        login_creds = {'username': user, 'password': password}
        _ = self.client.post(url='/user/create', json=login_creds)
        token = self.client.post(url='/user/auth', data=login_creds).json()['access_token']
        return {'Authorization': f'Bearer {token}'}

    def setUp(self) -> None:
        self.client = TestClient(app)
        db.user.drop()
        db.room.drop()

    def tearDown(self) -> None:
        db.user.drop()
        db.room.drop()

    @pytest.mark.integtest
    def test_join_no_pwd(self):
        headers_creator = self.create_and_auth_user('miles', 'abc')
        headers_joiner = self.create_and_auth_user('marcel', 'abc')
        data = {'room_name': 'test'}
        response = self.client.post(url='/room/create', json=data, headers=headers_creator)
        room_id = response.json()['room_id']
        response = self.client.post(url=f'/room/join/{room_id}',
                                    headers=headers_joiner, json={})
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('joined', response.json()['status'])

    @pytest.mark.integtest
    def test_rejoin(self):
        headers_creator = self.create_and_auth_user('miles', 'abc')
        data = {'room_name': 'test'}
        response = self.client.post(url='/room/create', json=data, headers=headers_creator)
        room_id = response.json()['room_id']
        response = self.client.post(url='/room/reconnect/',
                                    headers=headers_creator, json={})
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('joined', response.json()['status'])
        self.assertEqual(room_id, response.json()['room_id'])
