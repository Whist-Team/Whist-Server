import unittest

from starlette.testclient import TestClient

from whist.server import app


class LeaderboardTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.app = app

    def test_correct_des_order(self):
        data = {'order': 'descending'}
        response = self.client.get(url='/leaderboard', json=data)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertEqual([self.user.to_user(), self.second_user.to_user()], response['ranking'])

    def test_correct_asc_order(self):
        data = {'order': 'ascending'}
        response = self.client.get(url='/leaderboard', json=data)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertEqual([self.second_user.to_user(), self.user.to_user()], response['ranking'])
