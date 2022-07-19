from unittest.mock import MagicMock

from fastapi import status
from starlette.testclient import TestClient
from whist_core.user.player import Player

from tests.whist_server.base_token_case import TestCaseWithToken
from whist_server import app
from whist_server.const import INITIAL_RATING
from whist_server.database.user import UserInDb
from whist_server.services.error import UserNotFoundError
from whist_server.services.ranking_service import RankingService
from whist_server.services.user_db_service import UserDatabaseService


class LeaderboardTestCase(TestCaseWithToken):
    def setUp(self) -> None:
        super().setUp()
        self.user: UserInDb = UserInDb(username='test', hashed_password='abc')
        self.second_user = UserInDb(username='lower_ranking', rating=INITIAL_RATING - 10,
                                    hashed_password='abc')
        self.users_asc = [self.user.to_user(), self.second_user.to_user()]
        self.users_desc = [self.second_user.to_user(), self.user.to_user()]
        self.ranking_service_mock = MagicMock()
        app.dependency_overrides[RankingService] = lambda: self.ranking_service_mock

        self.client = TestClient(app)
        self.app = app

    def test_login_required(self):
        self.app.dependency_overrides = {}
        self.ranking_service_mock.select = MagicMock(return_value=self.users_desc)
        user_service = MagicMock(get=MagicMock(side_effect=UserNotFoundError))
        self.app.dependency_overrides[UserDatabaseService] = lambda: user_service
        response = self.client.get(url='/leaderboard/?order=descending&start=0&amount=0')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_correct_des_order(self):
        self.ranking_service_mock.select = MagicMock(return_value=self.users_desc)
        response = self.client.get(url='/leaderboard/?order=descending&start=0&amount=0')
        players = [Player(**player) for player in response.json()]
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.ranking_service_mock.select.assert_called_with('descending', 0, 0)
        self.assertEqual(self.users_desc, players)

    def test_correct_des_order_no_param(self):
        self.ranking_service_mock.select = MagicMock(return_value=self.users_desc)
        response = self.client.get(url='/leaderboard/?order=descending')
        players = [Player(**player) for player in response.json()]
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.ranking_service_mock.select.assert_called_with('descending', 0, 0)
        self.assertEqual(self.users_desc, players)

    def test_correct_asc_order(self):
        self.ranking_service_mock.select = MagicMock(return_value=self.users_asc)
        response = self.client.get(url='/leaderboard/?order=ascending&start=0&amount=0',
                                   headers=self.headers)
        players = [Player(**player) for player in response.json()]
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.ranking_service_mock.select.assert_called_with('ascending', 0, 0)
        self.assertEqual(self.users_asc, players)

    def test_correct_asc_order_limited(self):
        self.ranking_service_mock.select = MagicMock(return_value=[self.user.to_user()])
        response = self.client.get(url='/leaderboard/?order=ascending&start=0&amount=1',
                                   headers=self.headers)
        players = [Player(**player) for player in response.json()]
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.ranking_service_mock.select.assert_called_with('ascending', 1, 0)
        self.assertEqual([self.user.to_user()], players)

    def test_correct_asc_order_index(self):
        self.ranking_service_mock.select = MagicMock(return_value=[self.second_user.to_user()])
        response = self.client.get(url='/leaderboard/?order=ascending&start=1&amount=0',
                                   headers=self.headers)
        players = [Player(**player) for player in response.json()]
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.ranking_service_mock.select.assert_called_with('ascending', 0, 1)
        self.assertEqual([self.second_user.to_user()], players)
