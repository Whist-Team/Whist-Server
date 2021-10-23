from tests.whist.server.api.game.base_token_case import TestCaseWithToken


class JoinGameTestCase(TestCaseWithToken):

    def test_join_without_pwd(self):
        response = self.client.post(url='/game/join/')
        self.assertEqual(response.status_code, 200, msg=response.content)
