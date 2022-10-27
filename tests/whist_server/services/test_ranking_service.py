import pytest

from tests.whist_server.base_user_test_case import UserBaseTestCase
from whist_server.services.ranking_service import RankingService
from whist_server.services.user_db_service import UserDatabaseService


@pytest.mark.integtest
class LeaderboardTestCase(UserBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.ranking_service = RankingService()
        user_service = UserDatabaseService()
        user_service.add(self.user)
        user_service.add(self.second_user)

    def test_correct_des_order(self):
        ranking = self.ranking_service.select('descending', 0, 0)
        self.assertEqual([self.user.to_player(), self.second_user.to_player()], ranking)

    def test_correct_asc_order(self):
        ranking = self.ranking_service.select('ascending', 0, 0)
        self.assertEqual([self.second_user.to_player(), self.user.to_player()], ranking)

    def test_n_first(self):
        ranking = self.ranking_service.select(order='descending', amount=1, start=0)
        self.assertEqual([self.user.to_player()], ranking)

    def test_start_second(self):
        ranking = self.ranking_service.select(order='descending', amount=0, start=1)
        self.assertEqual([self.second_user.to_player()], ranking)
