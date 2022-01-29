from whist.core.cards.card import Card, Suit, Rank
from whist.core.cards.card_container import OrderedCardContainer
from whist.core.game.player_at_table import PlayerAtTable

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

    def test_not_players_turn(self):
        response = self.client.post(url=f'/game/trick/play_card/{self.game_id}',
                                    headers=self.second_player, json={'suit': 'clubs',
                                                                      'rank': 'ace'})
        self.assertEqual(400, response.status_code, msg=response.content)

    def test_winner(self):
        # Play Ace of Clubs
        _ = self.client.post(url=f'/game/trick/play_card/{self.game_id}',
                             headers=self.headers, json={'suit': 'clubs',
                                                         'rank': 'ace'})
        # Play King of Clubs
        _ = self.client.post(url=f'/game/trick/play_card/{self.game_id}',
                             headers=self.second_player, json={'suit': 'clubs',
                                                               'rank': 'king'})
        response = self.client.get(url=f'/game/trick/winner/{self.game_id}',
                                   headers=self.headers)
        self.assertEqual('marcel', PlayerAtTable(**response.json()).player.username)

    def test_no_winner_yet(self):
        # Play Ace of Clubs
        _ = self.client.post(url=f'/game/trick/play_card/{self.game_id}',
                             headers=self.headers, json={'suit': 'clubs',
                                                         'rank': 'ace'})
        response = self.client.get(url=f'/game/trick/winner/{self.game_id}',
                                   headers=self.headers)
        expected_message = 'The trick is not yet done, so there is no winner.'
        self.assertEqual(expected_message, response.json()['status'])
