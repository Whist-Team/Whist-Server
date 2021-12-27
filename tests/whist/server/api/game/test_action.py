from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase


class ActionGameTestCase(BaseCreateGameTestCase):
    def test_start(self):
        response = self.client.post(url=f'/game/action/start/{self.game_id}',
                                    headers=self.headers)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('started', response.json()['status'])

