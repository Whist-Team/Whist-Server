from unittest import TestCase
from unittest.mock import MagicMock

import pytest
from starlette.testclient import TestClient

from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase
from whist.server import app
from whist.server.database import db
from whist.server.database.warning import PlayerAlreadyJoinedWarning


class JoinGameTestCase(BaseCreateGameTestCase):

    def test_join(self):
        headers = self.create_and_auth_user('miles', 'abc')
        self.password_service_mock.verify = MagicMock(return_value=True)

        response = self.client.post(url=f'/game/join/{self.game_mock.id}',
                                    json={'password': 'abc'},
                                    headers=headers)
        self.game_mock.join.assert_called_once()
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('joined', response.json()['status'])

    def test_join_wrong_pwd_game(self):
        self.password_service_mock.verify = MagicMock(return_value=False)
        response = self.client.post(url=f'/game/join/{self.game_mock.id}',
                                    json={'password': 'abcd'},
                                    headers=self.headers)
        self.assertEqual(401, response.status_code, msg=response.content)

    def test_join_login_required(self):
        self.app.dependency_overrides = {}
        self.password_service_mock.verify = MagicMock(return_value=True)
        response = self.client.post(url=f'/game/join/{self.game_mock.id}',
                                    json={'password': 'abc'})
        self.assertEqual(401, response.status_code, msg=response.content)

    def test_host_join(self):
        self.game_mock.join = MagicMock(side_effect=PlayerAlreadyJoinedWarning)
        response = self.client.post(url=f'/game/join/{self.game_mock.id}',
                                    json={'password': 'abc'},
                                    headers=self.headers)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('already joined', response.json()['status'])


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
        data = {'game_name': 'test'}
        response = self.client.post(url='/game/create', json=data, headers=headers_creator)
        game_id = response.json()['game_id']
        response = self.client.post(url=f'/game/join/{game_id}',
                                    headers=headers_joiner, json={})
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('joined', response.json()['status'])
