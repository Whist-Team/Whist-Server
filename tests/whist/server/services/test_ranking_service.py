from tests.whist.server.services.base_user_test_case import UserBaseTestCase
from whist.server.const import INITIAL_RATING

from whist.server.database.user import UserInDb
from whist.server.services.ranking_service import RankingService, ASCENDING, DESCENDING
from whist.server.services.user_db_service import UserDatabaseService


class LeaderboardTestCase(UserBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.second_user = UserInDb(username='lower_ranking', rating=INITIAL_RATING - 10)
        self.ranking_service = RankingService()
        user_service = UserDatabaseService()
        user_service.add(self.user)
        user_service.add(self.second_user)

    def test_correct_des_order(self):
        ranking = self.ranking_service.all(DESCENDING)
        self.assertEqual([self.user.to_user(), self.second_user.to_user()], ranking)

    def test_correct_asc_order(self):
        ranking = self.ranking_service.all(ASCENDING)
        self.assertEqual([self.second_user.to_user(), self.user.to_user()], ranking)
