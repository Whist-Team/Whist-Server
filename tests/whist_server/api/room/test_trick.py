from unittest.mock import MagicMock, PropertyMock

from whist_core.cards.card import Card, Suit, Rank
from whist_core.cards.card_container import OrderedCardContainer
from whist_core.cards.card_container import UnorderedCardContainer
from whist_core.game.errors import NotPlayersTurnError
from whist_core.game.warnings import TrickNotDoneWarning

from tests.whist_server.api.room.base_created_case import BaseCreateGameTestCase
from whist_server import app


class TrickTestCase(BaseCreateGameTestCase):
    def setUp(self):
        super().setUp()
        self.first_card = Card(suit=Suit.CLUBS, rank=Rank.A)
        self.second_card = Card(suit=Suit.CLUBS, rank=Rank.K)

        self.hand = UnorderedCardContainer.with_cards([self.first_card, self.second_card])
        self.first_player_mock = MagicMock(hand=self.hand, player=MagicMock(), team=MagicMock())
        self.stack = OrderedCardContainer.with_cards(self.first_card)
        self.trick_mock = MagicMock(play_card=MagicMock(), stack=self.stack,
                                    done=False)
        self.room_mock.current_trick = MagicMock(return_value=self.trick_mock)
        self.room_mock.next_trick = MagicMock(return_value=self.trick_mock)
        self.room_mock.players = [self.player_mock]

    def test_player_hand(self):
        self.room_mock.get_player = MagicMock(return_value=self.first_player_mock)
        response = self.client.get(url=f'/room/trick/hand/{self.room_mock.id}',
                                   headers=self.headers)
        self.assertEqual(UnorderedCardContainer(**response.json()), self.hand)

    def test_play_card(self):
        response = self.client.post(url=f'/room/trick/play_card/{self.room_mock.id}',
                                    headers=self.headers, json=self.first_card.dict())
        self.assertEqual(200, response.status_code, msg=response.content)
        self.room_service_mock.save.assert_called_once()
        response_stack = OrderedCardContainer(**response.json())
        self.assertEqual(self.stack, response_stack)

    def test_not_players_turn(self):
        self.trick_mock.play_card = MagicMock(
            side_effect=NotPlayersTurnError(player=MagicMock(),
                                            turn_player=MagicMock()))
        response = self.client.post(url=f'/room/trick/play_card/{self.room_mock.id}',
                                    headers=self.headers, json=self.first_card.dict())
        self.assertEqual(400, response.status_code, msg=response.content)

    def test_winner(self):
        winner = PropertyMock(return_value=self.first_player_mock)
        type(self.trick_mock).winner = winner
        response = self.client.get(url=f'/room/trick/winner/{self.room_mock.id}',
                                   headers=self.headers)
        winner.assert_called_once()
        self.assertEqual(200, response.status_code)

    def test_no_winner_yet(self):
        winner = PropertyMock(side_effect=TrickNotDoneWarning)
        type(self.trick_mock).winner = winner
        response = self.client.get(url=f'/room/trick/winner/{self.room_mock.id}',
                                   headers=self.headers)
        expected_message = 'The trick is not yet done, so there is no winner.'
        self.assertEqual(expected_message, response.json()['status'])

    def test_not_joined_winner(self):
        self.room_mock.players = []
        response = self.client.get(url=f'/room/trick/winner/{self.room_mock.id}',
                                   headers=self.headers)
        self.assertEqual(403, response.status_code, msg=response.content)

    def test_next_trick(self):
        response = self.client.post(url=f'/room/next_trick/{self.room_mock.id}',
                                    headers=self.headers)
        self.room_mock.next_trick.assert_called_once()
        self.assertEqual('Success', response.json()['status'])
        self.assertEqual(200, response.status_code)

    def test_next_trick_without_user(self):
        app.dependency_overrides = {}
        response = self.client.post(url=f'/room/next_trick/{self.room_mock.id}')
        self.room_mock.next_trick.assert_not_called()
        self.assertEqual(401, response.status_code)
