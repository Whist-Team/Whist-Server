import unittest

from starlette.testclient import TestClient

from whist.server import app
from whist.server.database import db


class GameTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.login_creds = {'username': 'marcel', 'password': 'abc'}
        _ = self.client.post(url='/user/create', json=self.login_creds)
        token = self.client.post(url='/user/auth/', data=self.login_creds).json()['token']
        self.headers = {'Authorization': f'Bearer {token}'}

    def tearDown(self) -> None:
        db.game.drop()
        db.user.drop()

    def test_post_game(self):
        data = {'game_name': 'test', 'password': 'abc'}
        response = self.client.post(url='/game/create', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertTrue('game_id' in response.json())
        self.assertEqual(1, db.game.count())

    def test_post_game_without_pwd(self):
        data = {'game_name': 'test'}
        response = self.client.post(url='/game/create', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertTrue('game_id' in response.json())
        self.assertEqual(1, db.game.count())

    def test_post_game_without_name(self):
        data = {'password': 'abc'}
        response = self.client.post(url='/game/create', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 400, msg=response.content)
        self.assertEqual('"game_name" is required.', response.json()['detail'])
        self.assertEqual(0, db.game.count())
