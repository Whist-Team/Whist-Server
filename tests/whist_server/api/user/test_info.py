from whist_core.user.player import Player

from tests.whist_server.base_token_case import TestCaseWithToken


class UserInfoTestCase(TestCaseWithToken):
    def test_info(self):
        response = self.client.get(url='/user/info')
        self.assertEqual(self.player_mock, Player(**response.json()))
        self.assertEqual(200, response.status_code)
