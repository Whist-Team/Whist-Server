"""Errors occurring in a service class."""
from typing import Optional

from fastapi import HTTPException
from starlette import status


class GitHubAuthError(Exception):
    """
    Is raised when authentication with GitHub fails.
    """

    def __init__(self, error: str, error_description: str, error_uri: str):
        """
        Creates a new GitHub Authentication error. Wraps the HTTP error returned from GitHub.
        :param error: Type of the error.
        :param error_description: Detailed description.
        :param error_uri: The URL for help.
        """
        message = f'{error}: Details: {error_description}, Help: {error_uri}'
        super().__init__(message)


class UserExistsError(Exception):
    """
    Is raised when an user already exists.
    """


class UserNotReadyError(Exception):
    """
    Is raised when a user is not to start.
    """


class UserNotFoundError(Exception):
    """
    Is raised when a user is not found in the database.
    """

    def __init__(self, username: Optional[str] = None):
        """
        Constructor.
        :param username: OPTIONAL. name of the user not found.
        """
        if username:
            message = f'User with name "{username}" not found.'
        else:
            message = 'User not found.'
        super().__init__(message)


class RoomNotFoundError(Exception):
    """
    Is raised when the room is not found in db.
    """

    def __init__(self, game_id: Optional[str] = None, game_name: Optional[str] = None):
        """
        Constructor.
        :param game_id: ID of the room.
        :param game_name: Name of the room.
        """
        if game_id:
            message = f'Room with id "{game_id}" not found.'
        elif game_name:
            message = f'Room with name "{game_id}" not found.'
        else:
            message = 'Room not found'
        super().__init__(message)


class RoomNotUpdatedError(Exception):
    """
    Is raised when a room could not be updated to the database.
    """

    def __init__(self, game_id: str):
        """
        Constructor.
        :param game_id: ID of the room.
        """
        message = f'Room with id "{game_id}" could not be updated.'
        super().__init__(message)


class CredentialsException(HTTPException):
    """
    Is raised when the credentials are incorrect.
    """

    def __init__(self):
        """
        Constructor.
        """
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Could not validate credentials",
                         headers={"WWW-Authenticate": "Bearer"})


class ChannelAlreadyExistsError(Exception):
    """
    Is raised when a side channel already exists for that room.
    """


class ChannelNotFoundError(Exception):
    """
    Is raised when a side channel could not be found for that room.
    """
