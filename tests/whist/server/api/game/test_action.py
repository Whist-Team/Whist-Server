from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase
from whist.server.database import db
from whist.server.database.game import GameInDb
from whist.server.services.game_db_service import GameDatabaseService


class ActionGameTestCase(BaseCreateGameTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.second_player = self.create_and_auth_user('miles', 'abc')

    def test_start(self):
        # Mark the player ready
        _ = self.client.post(url=f'/game/action/ready/{self.game_id}',
                             headers=self.headers)
        # Request to start table.
        response = self.client.post(url=f'/game/action/start/{self.game_id}',
                                    headers=self.headers)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('started', response.json()['status'])

    def test_start_not_creator(self):
        # Create another user

        # New user mark theyself ready
        _ = self.client.post(url=f'/game/action/ready/{self.game_id}',
                             headers=self.second_player)

        # New user tries to start table.
        response = self.client.post(url=f'/game/action/start/{self.game_id}',
                                    headers=self.second_player)
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_start_table_not_ready(self):
        # Request to start table.
        response = self.client.post(url=f'/game/action/start/{self.game_id}',
                                    headers=self.headers)
        self.assertEqual(400, response.status_code, msg=response.content)

    def test_ready(self):
        response = self.client.post(url=f'/game/action/ready/{self.game_id}',
                                    headers=self.headers)
        game = GameInDb(**db.game.find()[0])
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertTrue(game.table.ready)

    def test_ready_not_joined(self):
        response = self.client.post(url=f'/game/action/ready/{self.game_id}',
                                    headers=self.second_player)
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_ready_second_player(self):
        game_service = GameDatabaseService()

        # Join second player
        _ = self.client.post(url=f'/game/join/{self.game_id}',
                             json={'password': 'abc'},
                             headers=self.second_player)
        # Ready first player
        _ = self.client.post(url=f'/game/action/ready/{self.game_id}',
                             headers=self.headers)
        # Ready second player
        response = self.client.post(url=f'/game/action/ready/{self.game_id}',
                                    headers=self.second_player)
        db_game = game_service.get(self.game_id)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertTrue(db_game.table.ready)
