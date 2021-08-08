"""Errors occurring in a service class."""


class UserNotFoundError(Exception):
    """
    Is raised when an user is not found in the database.
    """

    def __init__(self, user_id: str):
        message = f'User with id "{user_id}" not found.'
        super().__init__(message)
