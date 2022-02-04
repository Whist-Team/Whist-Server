from whist.core.cards.card import Card, Suit, Rank
from whist.core.cards.card_container import OrderedCardContainer
from whist.core.cards.card_container import UnorderedCardContainer
from whist.core.game.player_at_table import PlayerAtTable

from tests.whist.server.api.game.base_created_case import BaseCreateGameTestCase


class TrickTestCase(BaseCreateGameTestCase):
    def setUp(self):
        super().setUp()
        self.first_card = Card(suit=Suit.CLUBS, rank=Rank.A)
        self.second_card = Card(suit=Suit.CLUBS, rank=Rank.K)
        self.second_player = self.create_and_auth_user('miles', 'abc')
        self.third_player = self.create_and_auth_user('nico', 'abc')
        self.forth_player = self.create_and_auth_user('bot', 'abc')

        self.players = {'marcel': self.headers, 'miles': self.second_player,
                        'nico': self.third_player, 'bot': self.forth_player}
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
                             json={'matcher_type': 'robin'})

    def test_player_hand(self):
        response = self.client.get(url=f'/game/trick/hand/{self.game_id}',
                                   headers=self.headers)
        player_hand = UnorderedCardContainer(**response.json())
        self.assertEqual(13, len(player_hand.cards))

    def test_hand_different(self):
        response = self.client.get(url=f'/game/trick/hand/{self.game_id}',
                                   headers=self.headers)
        first_hand = UnorderedCardContainer(**response.json())
        response = self.client.get(url=f'/game/trick/hand/{self.game_id}',
                                   headers=self.second_player)
        second_hand = UnorderedCardContainer(**response.json())
        response = self.client.get(url=f'/game/trick/hand/{self.game_id}',
                                   headers=self.third_player)
        third_hand = UnorderedCardContainer(**response.json())
        response = self.client.get(url=f'/game/trick/hand/{self.game_id}',
                                   headers=self.forth_player)
        forth_hand = UnorderedCardContainer(**response.json())
        self.assertNotEqual(first_hand, second_hand)
        self.assertNotEqual(first_hand, third_hand)
        self.assertNotEqual(first_hand, forth_hand)

    def test_play_card(self):
        card_dict, response = self._play_first_card(self.headers)
        self.assertEqual(200, response.status_code, msg=response.content)

        expected_stack = OrderedCardContainer.empty()
        expected_stack.add(Card(**card_dict))
        response_stack = OrderedCardContainer(**response.json())
        self.assertEqual(expected_stack, response_stack)

    def test_play_second_card(self):
        first_card_dict, _ = self._play_first_card(self.headers)
        second_card_dict, response = self._play_first_card(self.second_player)
        self.assertEqual(200, response.status_code, msg=response.content)

        expected_stack = OrderedCardContainer.empty()
        expected_stack.add(Card(**first_card_dict))
        expected_stack.add(Card(**second_card_dict))
        response_stack = OrderedCardContainer(**response.json())
        self.assertEqual(expected_stack, response_stack)

    def test_not_players_turn(self):
        _, response = self._play_first_card(self.second_player)
        self.assertEqual(400, response.status_code, msg=response.content)

    def test_winner(self):
        _ = self._play_first_card(self.headers)
        _ = self._play_first_card(self.second_player)
        _ = self._play_first_card(self.third_player)
        _ = self._play_first_card(self.forth_player)
        response = self.client.get(url=f'/game/trick/winner/{self.game_id}',
                                   headers=self.headers)
        self.assertIsInstance(PlayerAtTable(**response.json()), PlayerAtTable)

    def test_no_winner_yet(self):
        _ = self._play_first_card(self.headers)
        response = self.client.get(url=f'/game/trick/winner/{self.game_id}',
                                   headers=self.headers)
        expected_message = 'The trick is not yet done, so there is no winner.'
        self.assertEqual(expected_message, response.json()['status'])

    def test_not_joined_winner(self):
        third_player = self.create_and_auth_user('third', 'third')
        # Play Ace of Clubs
        _ = self.client.post(url=f'/game/trick/play_card/{self.game_id}',
                             headers=self.headers, json={'suit': 'clubs',
                                                         'rank': 'ace'})
        # Play King of Clubs
        _ = self.client.post(url=f'/game/trick/play_card/{self.game_id}',
                             headers=self.second_player, json={'suit': 'clubs',
                                                               'rank': 'king'})
        response = self.client.get(url=f'/game/trick/winner/{self.game_id}',
                                   headers=third_player)
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_next_trick(self):
        _ = self._play_first_card(self.headers)
        _ = self._play_first_card(self.second_player)
        _ = self._play_first_card(self.third_player)
        _ = self._play_first_card(self.forth_player)
        response = self.client.get(url=f'/game/trick/winner/{self.game_id}',
                                   headers=self.headers)
        winner = PlayerAtTable(**response.json())
        winner_header = self.players[winner.player.username]
        card_dict, response = self._play_first_card(winner_header)

        self.assertEqual(200, response.status_code, msg=response.content)

        expected_stack = OrderedCardContainer.empty()
        expected_stack.add(Card(**card_dict))
        response_stack = OrderedCardContainer(**response.json())
        self.assertEqual(expected_stack, response_stack)

    def _play_first_card(self, player):
        response = self.client.get(url=f'/game/trick/hand/{self.game_id}',
                                   headers=player)
        hand = UnorderedCardContainer(**response.json())
        # Play Ace of Clubs
        card_dict = list(hand)[0].dict()
        response = self.client.post(url=f'/game/trick/play_card/{self.game_id}',
                                    headers=player, json=card_dict)
        return card_dict, response
