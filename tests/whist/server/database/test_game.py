from whist.core.cards.card import Card, Suit, Rank
from whist.core.cards.card_container import OrderedCardContainer
from whist.core.game.warnings import ServSuitFirstWarning
from whist.core.session.matcher import RoundRobinMatcher
from whist.core.user.player import Player

from tests.whist.server.base_player_test_case import BasePlayerTestCase
from whist.server.database.game import GameInDb
from whist.server.database.warning import PlayerAlreadyJoinedWarning
from whist.server.services.password import PasswordService


class GameInDbTestCase(BasePlayerTestCase):
    def setUp(self) -> None:
        super().setUp()
        password_service = PasswordService()
        self.game: GameInDb = GameInDb.create_with_pwd(game_name='test',
                                                       hashed_password=password_service.hash('abc'),
                                                       creator=self.player,
                                                       max_player=2,
                                                       min_player=2)
        self.second_player = Player(username='2', rating=1200)
        self.expected_players = [self.player, self.second_player]

    def test_verify_pwd(self):
        self.assertTrue(self.game.verify_password('abc'))

    def test_verify_fail(self):
        self.assertFalse(self.game.verify_password('bac'))

    def test_verify_without_password(self):
        game: GameInDb = GameInDb.create_with_pwd(game_name='test', creator=self.player)
        self.assertTrue(game.verify_password(None))

    def test_join(self):
        self.assertTrue(self.game.join(self.second_player))
        self.assertEqual(self.expected_players, self.game.players)

    def test_join_twice(self):
        self.assertTrue(self.game.join(self.second_player))
        with self.assertRaises(PlayerAlreadyJoinedWarning):
            self.assertTrue(self.game.join(self.second_player))
        self.assertEqual(self.expected_players, self.game.players)

    def test_play_card(self):
        self.game.ready_player(self.player)
        self.game.join(self.second_player)
        self.game.ready_player(self.second_player)
        self.game.start(self.player, RoundRobinMatcher)
        card = Card(suit=Suit.CLUBS, rank=Rank.A)
        trick = self.game.current_trick()
        player = self.game.get_player(self.player)
        trick.play_card(player=player, card=card)
        expected_stack = OrderedCardContainer.empty()
        expected_stack.add(card)
        self.assertEqual(expected_stack, self.game.current_stack)

    def test_play_second_card(self):
        self.game.ready_player(self.player)
        self.game.join(self.second_player)
        self.game.ready_player(self.second_player)
        self.game.start(self.player, RoundRobinMatcher)
        first_card = Card(suit=Suit.CLUBS, rank=Rank.A)
        second_card = Card(suit=Suit.CLUBS, rank=Rank.K)
        trick = self.game.current_trick()
        first_player = self.game.get_player(self.player)
        second_player = self.game.get_player(self.second_player)
        trick.play_card(player=first_player, card=first_card)
        trick.play_card(player=second_player, card=second_card)
        expected_stack = OrderedCardContainer.empty()
        expected_stack.add(first_card)
        expected_stack.add(second_card)
        self.assertEqual(expected_stack, self.game.current_stack)

    def test_play_illegal_card(self):
        self.game.ready_player(self.player)
        self.game.join(self.second_player)
        self.game.ready_player(self.second_player)
        self.game.start(self.player, RoundRobinMatcher)
        first_card = Card(suit=Suit.CLUBS, rank=Rank.A)
        second_card = Card(suit=Suit.HEARTS, rank=Rank.K)
        trick = self.game.current_trick()
        first_player = self.game.get_player(self.player)
        second_player = self.game.get_player(self.second_player)
        trick.play_card(player=first_player, card=first_card)
        expected_stack = OrderedCardContainer.empty()
        expected_stack.add(first_card)
        with self.assertRaises(ServSuitFirstWarning):
            trick.play_card(player=second_player, card=second_card)
        self.assertEqual(expected_stack, self.game.current_stack)
