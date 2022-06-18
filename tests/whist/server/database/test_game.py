from unittest.mock import MagicMock, PropertyMock, patch

from whist.core.cards.card_container import UnorderedCardContainer
from whist.core.session.matcher import RandomMatcher
from whist.core.user.player import Player

from tests.whist.server.base_player_test_case import BasePlayerTestCase
from whist.server.database.error import PlayerNotCreatorError
from whist.server.database.game import GameInDb
from whist.server.database.warning import PlayerAlreadyJoinedWarning
from whist.server.services.game_db_service import GameDatabaseService
from whist.server.services.password import PasswordService


class GameInDbTestCase(BasePlayerTestCase):
    def setUp(self) -> None:
        super().setUp()
        password_service = PasswordService()
        self.game_service = GameDatabaseService()
        self.game: GameInDb = self.game_service.create_with_pwd(
            game_name='test',
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
        game: GameInDb = self.game_service.create_with_pwd(game_name='test', creator=self.player)
        self.assertTrue(game.verify_password(None))

    @patch('whist.server.web_socket.subscriber.Subscriber')
    def test_join(self, subscriber_mock: MagicMock):
        self.game.side_channel.attach(subscriber_mock)
        self.assertTrue(self.game.join(self.second_player))
        self.assertEqual(self.expected_players, self.game.players)
        subscriber_mock.send.assert_called_once()

    def test_join_twice(self):
        self.assertTrue(self.game.join(self.second_player))
        with self.assertRaises(PlayerAlreadyJoinedWarning):
            self.assertTrue(self.game.join(self.second_player))
        self.assertEqual(self.expected_players, self.game.players)

    def test_has_joined(self):
        self.assertTrue(self.game.has_joined(self.player))

    def has_not_joined(self):
        self.assertFalse(self.game.has_joined(self.second_player))

    def test_auto_next(self):
        self.game.table = MagicMock(started=PropertyMock(return_value=True))
        first_trick = self.game.current_trick()
        second_trick = self.game.current_trick(auto_next=True)
        self.assertNotEqual(first_trick, second_trick)

    def test_auto_next_off(self):
        self.game.table = MagicMock(started=PropertyMock(return_value=True))
        first_trick = self.game.current_trick()
        second_trick = self.game.current_trick(auto_next=False)
        self.assertEqual(first_trick, second_trick)

    def test_start_not_creator(self):
        with self.assertRaises(PlayerNotCreatorError):
            self.game.start(player=self.second_player, matcher=RandomMatcher())

    def test_get_player(self):
        play_at_table_mock = MagicMock(player=PropertyMock(return_value=self.player),
                                       hand=UnorderedCardContainer.empty(), team=MagicMock())
        game_mock = MagicMock(get_player=MagicMock(return_value=play_at_table_mock))
        self.game.table = MagicMock(ready=PropertyMock(return_value=True),
                                    current_rubber=PropertyMock(games=[game_mock]))
        player_at_table = self.game.get_player(self.player)
        self.assertEqual(play_at_table_mock, player_at_table)
