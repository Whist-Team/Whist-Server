from unittest.mock import MagicMock

from starlette.testclient import TestClient

from tests.whist.server.base_user_test_case import UserBaseTestCase
from whist.server import app
from whist.server.services.ranking_service import RankingService


class LeaderboardTestCase(UserBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.users_asc = [self.user.to_user(), self.second_user.to_user()]
        self.ranking_service_mock = MagicMock(all=self.users_asc)
        app.dependency_overrides[RankingService] = lambda: self.ranking_service_mock

        self.client = TestClient(app)
        self.app = app

    def test_correct_des_order(self):
        response = self.client.get(url='/leaderboard/descending')
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertEqual(self.users_asc, response['ranking'])

    def test_correct_asc_order(self):
        response = self.client.get(url='/leaderboard/ascending')
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertEqual([self.second_user.to_user(), self.user.to_user()], response['ranking'])
