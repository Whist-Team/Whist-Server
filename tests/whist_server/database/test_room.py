from unittest.mock import MagicMock, PropertyMock

from whist_core.cards.card_container import UnorderedCardContainer
from whist_core.session.matcher import RandomMatcher
from whist_core.user.player import Player

from tests.whist_server.base_player_test_case import BasePlayerTestCase
from whist_server.database.error import PlayerNotCreatorError
from whist_server.database.room import RoomInDb, RoomInfo
from whist_server.database.warning import PlayerAlreadyJoinedWarning
from whist_server.services.password import PasswordService
from whist_server.services.room_db_service import RoomDatabaseService


class RoomInDbTestCase(BasePlayerTestCase):
    def setUp(self) -> None:
        super().setUp()
        password_service = PasswordService()
        self.room_service = RoomDatabaseService()
        self.room: RoomInDb = self.room_service.create_with_pwd(
            room_name='test',
            hashed_password=password_service.hash('abc'),
            creator=self.player,
            max_player=2,
            min_player=2)
        self.second_player = Player(username='2', rating=1200)
        self.expected_players = [self.player, self.second_player]

    def test_verify_pwd(self):
        self.assertTrue(self.room.verify_password('abc'))

    def test_verify_fail(self):
        self.assertFalse(self.room.verify_password('bac'))

    def test_verify_without_password(self):
        room: RoomInDb = self.room_service.create_with_pwd(room_name='test', creator=self.player)
        self.assertTrue(room.verify_password(None))

    def test_join(self):
        self.assertTrue(self.room.join(self.second_player))
        self.assertEqual(self.expected_players, self.room.players)

    def test_join_twice(self):
        self.assertTrue(self.room.join(self.second_player))
        with self.assertRaises(PlayerAlreadyJoinedWarning):
            self.assertTrue(self.room.join(self.second_player))
        self.assertEqual(self.expected_players, self.room.players)

    def test_has_joined(self):
        self.assertTrue(self.room.has_joined(self.player))

    def has_not_joined(self):
        self.assertFalse(self.room.has_joined(self.second_player))

    def test_next(self):
        self.room.table = MagicMock(started=PropertyMock(return_value=True))
        first_trick = self.room.current_trick()
        second_trick = self.room.next_trick()
        self.assertNotEqual(first_trick, second_trick)

    def test_start_not_creator(self):
        with self.assertRaises(PlayerNotCreatorError):
            self.room.start(player=self.second_player, matcher=RandomMatcher())

    def test_get_player(self):
        play_at_table_mock = MagicMock(player=PropertyMock(return_value=self.player),
                                       hand=UnorderedCardContainer.empty(), team=MagicMock())
        game_mock = MagicMock(get_player=MagicMock(return_value=play_at_table_mock))
        self.room.table = MagicMock(ready=PropertyMock(return_value=True),
                                    current_rubber=PropertyMock(games=[game_mock]))
        player_at_table = self.room.get_player(self.player)
        self.assertEqual(play_at_table_mock, player_at_table)

    def test_room_info(self):
        room_info = self.room.get_info()
        expected_info = RoomInfo(name='test', password=True, rubber_number=0,
                                 game_number=0, hand_number=0, trick_number=0, min_player=2,
                                 max_player=2, player_number=1)
        self.assertEqual(expected_info, room_info)

    def test_room_info_no_pwd(self):
        self.room.hashed_password = None
        room_info = self.room.get_info()
        expected_info = RoomInfo(name='test', password=False, rubber_number=0,
                                 game_number=0, hand_number=0, trick_number=0, min_player=2,
                                 max_player=2, player_number=1)
        self.assertEqual(expected_info, room_info)
