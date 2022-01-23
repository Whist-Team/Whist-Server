from whist.core.cards.card import Card, Suit, Rank
from whist.core.cards.card_container import OrderedCardContainer

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
        print(_)

    def test_play_card(self):
        # Play Ace of Clubs
        response = self.client.post(url=f'/game/trick/play_card/{self.game_id}',
                                    headers=self.headers, json={'suit': 'clubs',
                                                                'rank': 'ace'})
        self.assertEqual(200, response.status_code, msg=response.content)

        expected_stack = OrderedCardContainer.empty()
        expected_stack.add(self.first_card)
        response_stack = OrderedCardContainer(**response.json())
        self.assertEqual(expected_stack, response_stack)

    def test_play_second_card(self):
        # Play Ace of Clubs
        _ = self.client.post(url=f'/game/trick/play_card/{self.game_id}',
                             headers=self.headers, json={'suit': 'clubs',
                                                         'rank': 'ace'})
        # Play King of Clubs
        response = self.client.post(url=f'/game/trick/play_card/{self.game_id}',
                                    headers=self.second_player, json={'suit': 'clubs',
                                                                      'rank': 'king'})
        self.assertEqual(200, response.status_code, msg=response.content)

        expected_stack = OrderedCardContainer.empty()
        expected_stack.add(self.first_card)
        expected_stack.add(self.second_card)
        response_stack = OrderedCardContainer(**response.json())
        self.assertEqual(expected_stack, response_stack)
