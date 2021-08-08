"""Errors occurring in a service class."""


class UserNotFoundError(Exception):
    """
    Is raised when an user is not found in the database.
    """

    def __init__(self, user_id: str):
        message = f'User with id "{user_id}" not found.'
        super().__init__(message)


class GameInfoNotSet(Exception):
    """
    Is raised when the game info is not set.
    """

    def __init__(self):
        message = f'Game info is not set.'
        super().__init__(message)
