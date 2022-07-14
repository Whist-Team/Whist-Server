from tests.whist.server.base_user_test_case import UserBaseTestCase

from whist.server.services.ranking_service import RankingService
from whist.server.services.user_db_service import UserDatabaseService


class LeaderboardTestCase(UserBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.ranking_service = RankingService()
        user_service = UserDatabaseService()
        user_service.add(self.user)
        user_service.add(self.second_user)

    def test_correct_des_order(self):
        ranking = self.ranking_service.all('descending')
        self.assertEqual([self.user.to_user(), self.second_user.to_user()], ranking)

    def test_correct_asc_order(self):
        ranking = self.ranking_service.all('ascending')
        self.assertEqual([self.second_user.to_user(), self.user.to_user()], ranking)

    def test_n_first(self):
        ranking = self.ranking_service.select(order='descending', amount=1)
        self.assertEqual([self.user.to_user()], ranking)

    def test_start_second(self):
        ranking = self.ranking_service.select(order='descending', start=1)
        self.assertEqual([self.second_user.to_user()], ranking)
