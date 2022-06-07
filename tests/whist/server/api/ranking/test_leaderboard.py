from unittest.mock import MagicMock

from starlette.testclient import TestClient
from whist.core.user.player import Player

from tests.whist.server.base_user_test_case import UserBaseTestCase
from whist.server import app
from whist.server.services.ranking_service import RankingService


class LeaderboardTestCase(UserBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.users_asc = [self.user.to_user(), self.second_user.to_user()]
        self.users_desc = [self.second_user.to_user(), self.user.to_user()]
        self.ranking_service_mock = MagicMock()
        app.dependency_overrides[RankingService] = lambda: self.ranking_service_mock

        self.client = TestClient(app)
        self.app = app

    def test_correct_des_order(self):
        self.ranking_service_mock.all = MagicMock(return_value=self.users_desc)
        response = self.client.get(url='/leaderboard/descending')
        players = [Player(**player) for player in response.json()]
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.ranking_service_mock.all.assert_called_with('descending')
        self.assertEqual(self.users_desc, players)

    def test_correct_asc_order(self):
        self.ranking_service_mock.all = MagicMock(return_value=self.users_asc)
        response = self.client.get(url='/leaderboard/ascending')
        players = [Player(**player) for player in response.json()]
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.ranking_service_mock.all.assert_called_with('ascending')
        self.assertEqual(self.users_asc, players)
