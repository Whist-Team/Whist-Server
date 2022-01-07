from whist.core.cards.card import Card, Suit, Rank
from whist.core.cards.stack import Stack
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
        self.game.start(self.player)
        card = Card(Suit.CLUBS, Rank.A)
        player = self.game.current_rubber.next_game().next_hand()._current_play_order._play_order[
            0].player
        self.game.play_card(player, card)
        expected_stack = Stack()
        expected_stack.add(card)
        self.assertEqual(expected_stack, self.game.current_stack)

    def test_play_second_card(self):
        self.game.ready_player(self.player)
        self.game.join(self.second_player)
        self.game.ready_player(self.second_player)
        self.game.start(self.player)
        first_card = Card(Suit.CLUBS, Rank.A)
        second_card = Card(Suit.CLUBS, Rank.K)
        play_order = self.game.current_rubber.next_game().next_hand()._current_play_order._play_order
        first_player = play_order[0].player
        second_player = play_order[1].player
        self.game.play_card(first_player, first_card)
        self.game.play_card(second_player, second_card)
        expected_stack = Stack()
        expected_stack.add(first_card)
        expected_stack.add(second_card)
        self.assertEqual(expected_stack, self.game.current_stack)
