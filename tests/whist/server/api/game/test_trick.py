from whist.core.cards.card import Card, Suit, Rank
from whist.core.cards.stack import Stack

from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase


class TrickTestCase(BaseCreateGameTestCase):
    def test_play_card(self):
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
        first_card = Card(Suit.CLUBS, Rank.A)
        # Play Ace of Clubs
        response = self.client.post(url=f'/game/trick/play_card/{self.game_id}',
                                    headers=self.headers, json={'card': Card(Suit.CLUBS, Rank.A)})
        self.assertEqual(200, response.status_code, msg=response.content)

        expected_stack = Stack()
        expected_stack.add(first_card)
        self.assertEqual(expected_stack, response['stack'])
