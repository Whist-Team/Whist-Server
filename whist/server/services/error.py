"""Errors occurring in a service class."""
from fastapi import HTTPException
from starlette import status


class UserNotFoundError(Exception):
    """
    Is raised when an user is not found in the database.
    """

    def __init__(self, user_id: str):
        message = f'User with id "{user_id}" not found.'
        super().__init__(message)


class GameInfoNotSetError(Exception):
    """
    Is raised when the game info is not set.
    """

    def __init__(self):
        message = 'Game info is not set.'
        super().__init__(message)


class CredentialsException(HTTPException):
    """
    Is raised when the credentials are incorrect.
    """

    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Could not validate credentials",
                         headers={"WWW-Authenticate": "Bearer"})
