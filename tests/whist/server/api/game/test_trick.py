from whist.core.cards.card_container import UnorderedCardContainer

from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase


class TrickTestCase(BaseCreateGameTestCase):
    def setUp(self):
        super().setUp()
        self.second_player = self.create_and_auth_user('miles', 'abc')
        self.third_player = self.create_and_auth_user('nico', 'abc')
        self.forth_player = self.create_and_auth_user('bot', 'abc')

        # Join the second player
        _ = self.client.post(url=f'/game/join/{self.game_id}',
                             json={'password': 'abc'},
                             headers=self.second_player)
        # Join the third player
        _ = self.client.post(url=f'/game/join/{self.game_id}',
                             json={'password': 'abc'},
                             headers=self.third_player)
        # Join the forth player
        _ = self.client.post(url=f'/game/join/{self.game_id}',
                             json={'password': 'abc'},
                             headers=self.forth_player)
        # Mark the first player ready
        _ = self.client.post(url=f'/game/action/ready/{self.game_id}',
                             headers=self.headers)
        # Mark the second player ready
        _ = self.client.post(url=f'/game/action/ready/{self.game_id}',
                             headers=self.second_player)
        # Mark the third player ready
        _ = self.client.post(url=f'/game/action/ready/{self.game_id}',
                             headers=self.third_player)
        # Mark the forth player ready
        _ = self.client.post(url=f'/game/action/ready/{self.game_id}',
                             headers=self.forth_player)
        # Request to start table.
        _ = self.client.post(url=f'/game/action/start/{self.game_id}',
                             headers=self.headers,
                             json={'matcher_typer': 'robin'})

    def test_player_hand(self):
        response = self.client.get(url=f'/game/trick/hand/{self.game_id}',
                                   headers=self.headers)
        player_hand = UnorderedCardContainer(**response.json())
        self.assertEqual(13, len(player_hand.cards))
