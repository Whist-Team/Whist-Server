from whist.core.cards.card import Card, Suit, Rank
from whist.core.cards.card_container import OrderedCardContainer

from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase


class TrickTestCase(BaseCreateGameTestCase):
    def setUp(self):
        super().setUp()
        # Join the player
        _ = self.client.post(url=f'/game/join/{self.game_id}',
                             json={'password': 'abcd'},
                             headers=self.headers)
        # Mark the player ready
        _ = self.client.post(url=f'/game/action/ready/{self.game_id}',
                             headers=self.headers)
        # Request to start table.
        _ = self.client.post(url=f'/game/action/start/{self.game_id}',
                             headers=self.headers)

    def test_play_card(self):
        first_card = Card(suit=Suit.CLUBS, rank=Rank.A)
        # Play Ace of Clubs
        response = self.client.post(url=f'/game/trick/play_card/{self.game_id}',
                                    headers=self.headers, json={'suit': 'clubs',
                                                                'rank': 'ace'})
        self.assertEqual(200, response.status_code, msg=response.content)

        expected_stack = OrderedCardContainer.empty()
        expected_stack.add(first_card)
        response_stack = OrderedCardContainer(**response.json())
        self.assertEqual(expected_stack, response_stack)