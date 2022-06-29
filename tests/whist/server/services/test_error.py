from unittest import TestCase

from whist.server.services.error import UserNotFoundError, RoomNotFoundError


class UserNotFoundTestCase(TestCase):
    def test_user_not_found_error(self):
        error = UserNotFoundError()
        self.assertEqual('User not found.', error.args[0])


class GameNotFoundTestCase(TestCase):
    def test_game_not_found_error(self):
        game_id = '1'
        error = RoomNotFoundError(game_id)
        self.assertEqual(f'Game with id "{game_id}" not found.', error.args[0])
