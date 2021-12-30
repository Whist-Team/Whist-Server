"""Errors occurring in a service class."""
from typing import Optional

from fastapi import HTTPException
from starlette import status


class UserExistsError(Exception):
    """
    Is raised when an user already exists.
    """


class UserNotFoundError(Exception):
    """
    Is raised when an user is not found in the database.
    """

    def __init__(self, username: Optional[str] = None):
        if username:
            message = f'User with name "{username}" not found.'
        else:
            message = 'User not found.'
        super().__init__(message)


class GameInfoNotSetError(Exception):
    """
    Is raised when the game info is not set.
    """

    def __init__(self):
        message = 'Game info is not set.'
        super().__init__(message)


class GameNotFoundError(Exception):
    """
    Is raised when the game is not found in db.
    """

    def __init__(self, game_id: Optional[str] = None, game_name: Optional[str] = None):
        if game_id:
            message = f'Game with id "{game_id}" not found.'
        elif game_name:
            message = f'Game with name "{game_id}" not found.'
        else:
            message = 'Game not found'
        super().__init__(message)


class GameNotUpdatedError(Exception):
    """
    Is raised when a game could not be updated to the database.
    """

    def __init__(self, game_id: str):
        message = f'Game with id "{game_id}" could not be updated.'
        super().__init__(message)


class CredentialsException(HTTPException):
    """
    Is raised when the credentials are incorrect.
    """

    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Could not validate credentials",
                         headers={"WWW-Authenticate": "Bearer"})
