from tests.whist.server.api.game.base_token_case import TestCaseWithToken
from whist.server.database import db
from whist.server.database.game import GameInDb


class CreateGameTestCase(TestCaseWithToken):

    def test_post_game(self):
        data = {'game_name': 'test', 'password': 'abc'}
        response = self.client.post(url='/game/create', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertTrue('game_id' in response.json())
        self.assertEqual(1, db.game.estimated_document_count())

    def test_post_game_without_pwd(self):
        data = {'game_name': 'test'}
        response = self.client.post(url='/game/create', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertTrue('game_id' in response.json())
        self.assertEqual(1, db.game.estimated_document_count())

    def test_post_game_without_name(self):
        data = {'password': 'abc'}
        response = self.client.post(url='/game/create', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 400, msg=response.content)
        self.assertEqual('"game_name" is required.', response.json()['detail'])
        self.assertEqual(0, db.game.estimated_document_count())

    def test_post_game_with_settings(self):
        data = {'game_name': 'test', 'password': 'abc', 'min_player': 1, 'max_player': 1}
        response = self.client.post(url='/game/create', json=data, headers=self.headers)
        game = GameInDb(**db.game.find()[0])
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertTrue('game_id' in response.json())
        self.assertEqual(1, db.game.estimated_document_count())
        self.assertEqual(1, game.table.min_player, msg=f'min_player is {game.table.min_player} '
                                                       f'instead of 1')
        self.assertEqual(1, game.table.max_player, msg=f'max_player is {game.table.max_player} '
                                                       f'instead of 1')
