import unittest

from starlette.testclient import TestClient

from whist.server import app
from whist.server.database import db


class GameTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def tearDown(self) -> None:
        db.game.drop()

    def test_post_game(self):
        data = {'game_name': 'test', 'password': 'abc'}
        response = self.client.post(url='/game/create', json=data)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertTrue('game_id' in response.json())
        self.assertEqual(1, db.game.count())

    def test_post_game_without_pwd(self):
        data = {'game_name': 'test'}
        response = self.client.post(url='/game/create', json=data)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertTrue('game_id' in response.json())
        self.assertEqual(1, db.game.count())

    def test_post_game_without_name(self):
        data = {'password': 'abc'}
        response = self.client.post(url='/game/create', json=data)
        self.assertEqual(response.status_code, 400, msg=response.content)
        self.assertEqual('"game_name" is required.', response.json()['detail'])
        self.assertEqual(0, db.game.count())
