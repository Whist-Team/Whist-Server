from whist.core.cards.card import Card, Suit, Rank
from whist.core.cards.card_container import UnorderedCardContainer

from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase


class TrickTestCase(BaseCreateGameTestCase):
    def setUp(self):
        super().setUp()
        self.first_card = Card(suit=Suit.CLUBS, rank=Rank.A)
        self.second_card = Card(suit=Suit.CLUBS, rank=Rank.K)
        self.second_player = self.create_and_auth_user('miles', 'abc')

        # Join the second player
        _ = self.client.post(url=f'/game/join/{self.game_id}',
                             json={'password': 'abc'},
                             headers=self.second_player)
        # Mark the first player ready
        _ = self.client.post(url=f'/game/action/ready/{self.game_id}',
                             headers=self.headers)
        # Mark the second player ready
        _ = self.client.post(url=f'/game/action/ready/{self.game_id}',
                             headers=self.second_player)
        # Request to start table.
        _ = self.client.post(url=f'/game/action/start/{self.game_id}',
                             headers=self.headers,
                             json={'matcher_typer': 'robin'})

    def test_player_hand(self):
        response = self.client.get(url=f'/game/trick/hand/{self.game_id}',
                                   headers=self.headers)
        player_hand = UnorderedCardContainer(**response.json())
        self.assertEqual(13, len(player_hand.cards))
