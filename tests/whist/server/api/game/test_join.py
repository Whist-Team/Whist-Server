from unittest.mock import MagicMock

from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase
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
