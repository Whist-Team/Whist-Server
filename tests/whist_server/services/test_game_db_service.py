from unittest.mock import patch, MagicMock

from bson import ObjectId
from whist_core.session.matcher import RandomMatcher, RoundRobinMatcher
from whist_core.user.player import Player

from tests.whist_server.base_player_test_case import BasePlayerTestCase
from whist_server.services.error import RoomNotFoundError, RoomNotUpdatedError
from whist_server.services.room_db_service import RoomDatabaseService


class GameDdServiceTestCase(BasePlayerTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.room_db_mock = MagicMock()
        self.room = MagicMock(creator=self.player)
        self.id_mock = MagicMock(inserted_id='1' * 24)
        with patch('whist_server.database.db.room', self.room_db_mock):
            self.service = RoomDatabaseService()

    def test_add(self):
        self.room_db_mock.find_one = MagicMock(return_value=None)
        self.room_db_mock.insert_one = MagicMock(return_value=self.id_mock)
        game_id = self.service.add(self.room)
        self.room.id = ObjectId(game_id)
        self.room_db_mock.find_one = MagicMock(return_value=self.room)
        self.assertEqual(self.room, self.service.get(game_id))


def test_add_duplicate(self):
    game_id_first = self.service.add(self.room)
    game_id_second = self.service.add(self.room)
    self.assertEqual(game_id_first, game_id_second)


def test_not_existing(self):
    game_id = '1' * 24
    error_msg = f'Room with id "{game_id}" not found.'
    with self.assertRaisesRegex(RoomNotFoundError, error_msg):
        self.service.get(game_id)


def test_get_by_name(self):
    game_id = self.service.add(self.room)
    self.room.id = ObjectId(game_id)
    self.assertEqual(self.room, self.service.get_by_name('test'))


def test_save(self):
    game_id = self.service.add(self.room)
    self.room.id = game_id
    self.room.table.min_player = 3
    self.service.save(self.room)
    game = self.service.get(game_id)
    self.assertEqual(3, game.table.min_player)


def test_save_wrong_id(self):
    _ = self.service.add(self.room)
    self.room.id = '1' * 24
    self.room.table.min_player = 3
    with self.assertRaises(RoomNotFoundError):
        self.service.save(self.room)


@patch('pymongo.results.UpdateResult.modified_count', return_value=1)
def test_save_update_error(self, result_mock):
    game_id = self.service.add(self.room)
    self.room.id = game_id
    self.room.table.min_player = 3
    with self.assertRaises(RoomNotUpdatedError):
        self.service.save(self.room)


def test_save_started_table(self):
    game_id = self.service.add(self.room)
    self.room.id = game_id
    self.room.table.min_player = 2
    self.room.ready_player(self.player)
    second_player = Player(username='miles', rating=3000)
    self.room.join(second_player)
    self.room.ready_player(second_player)
    self.room.start(self.player, RandomMatcher)
    self.service.save(self.room)
    db_game = self.service.get(game_id)
    self.assertTrue(self.room.table.started)
    self.assertTrue(db_game.table.started)


def test_save_play_card(self):
    game_id = self.service.add(self.room)
    self.room.id = game_id
    self.room.table.min_player = 2
    self.room.ready_player(self.player)
    second_player = Player(username='miles', rating=3000)
    self.room.join(second_player)
    self.room.ready_player(second_player)
    self.room.start(self.player, RoundRobinMatcher)
    self.service.save(self.room)
    game = self.room.table.current_rubber.current_game()
    player = game.get_player(self.player)
    trick = game.next_hand().current_trick
    trick.play_card(player, player.hand.cards[0])
    self.service.save(self.room)


def test_all(self):
    game_id = self.service.add(self.room)
    self.room.id = game_id
    all_games = self.service.all()
    self.assertEqual(1, len(all_games))
    self.assertEqual(game_id, str(all_games[0].id))
