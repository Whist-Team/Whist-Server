from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase
from whist.server.database import db
from whist.server.database.game import GameInDb
from whist.server.services.game_db_service import GameDatabaseService


class ActionGameTestCase(BaseCreateGameTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.game_service = GameDatabaseService()

    def test_start(self):
        # Join the player
        _ = self.client.post(url=f'/game/join/{self.game_id}',
                             json={'password': 'abcd'},
                             headers=self.headers)
        # Mark the player ready
        _ = self.client.post(url=f'/game/action/ready/{self.game_id}',
                             headers=self.headers)
        # Request to start table.
        response = self.client.post(url=f'/game/action/start/{self.game_id}',
                                    headers=self.headers)
        db_game = self.game_service.get(self.game_id)

        self.assertTrue(db_game.table.started)
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertEqual('started', response.json()['status'])

    def test_start_not_creator(self):
        # Create another user
        headers = self.create_and_auth_user('miles', 'abc')

        # Join new user
        _ = self.client.post(url=f'/game/join/{self.game_id}',
                             json={'password': 'abcd'},
                             headers=headers)

        # New user mark theyself ready
        _ = self.client.post(url=f'/game/action/ready/{self.game_id}',
                             headers=headers)

        # New user tries to start table.
        response = self.client.post(url=f'/game/action/start/{self.game_id}',
                                    headers=headers)
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_start_table_not_ready(self):
        # Join the player
        _ = self.client.post(url=f'/game/join/{self.game_id}',
                             json={'password': 'abcd'},
                             headers=self.headers)
        # Request to start table.
        response = self.client.post(url=f'/game/action/start/{self.game_id}',
                                    headers=self.headers)
        self.assertEqual(400, response.status_code, msg=response.content)

    def test_ready(self):
        _ = self.client.post(url=f'/game/join/{self.game_id}',
                             json={'password': 'abcd'},
                             headers=self.headers)
        response = self.client.post(url=f'/game/action/ready/{self.game_id}',
                                    headers=self.headers)
        game = GameInDb(**db.game.find()[0])
        self.assertEqual(200, response.status_code, msg=response.content)
        self.assertTrue(game.table.ready)

    def test_ready_not_joined(self):
        headers = self.create_and_auth_user('miles', 'abc')
        response = self.client.post(url=f'/game/action/ready/{self.game_id}',
                                    headers=headers)
        self.assertEqual(403, response.status_code, msg=response.content)
