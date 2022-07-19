from unittest import TestCase

from whist_server.services.error import UserNotFoundError, RoomNotFoundError


class UserNotFoundTestCase(TestCase):
    def test_user_not_found_error(self):
        error = UserNotFoundError()
        self.assertEqual('User not found.', error.args[0])


class GameNotFoundTestCase(TestCase):
    def test_game_not_found_error(self):
        room_id = '1'
        error = RoomNotFoundError(room_id)
        self.assertEqual(f'Room with id "{room_id}" not found.', error.args[0])
