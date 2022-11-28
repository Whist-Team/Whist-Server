"""Token authentication"""
from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode
from whist_core.user.player import Player

from whist_server.const import SECRET_KEY, ALGORITHM
from whist_server.database.token import TokenData
from whist_server.services.error import CredentialsException
from whist_server.services.password import PasswordService
from whist_server.services.user_db_service import UserDatabaseService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/auth')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates an access token for an user.
    :param data: Expects a dictionary with key 'sub' and a username as value.
    :param expires_delta: The amount of time until this token shall expire.
    :return: token as a str
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme),
                           user_db_service=Depends(UserDatabaseService)) -> Player:
    """
    Retrieves the user from a token.
    :param token: access token
    :param user_db_service: service to handle request to the database storing users.
    :return: DO of User
    """
    token_data = await _get_token_data(token)
    user = user_db_service.get_by_username(token_data.username)
    return user


async def check_credentials(username: str, password: str) -> bool:
    """
    Verifies the password for a given username.
    :param username: the name of the user as string
    :param password: the plain password to be checked as string.
    :return: True if credentials are valid else False. If user not found raises
    UserNotFoundError.
    """
    user_db_service = UserDatabaseService()
    user = user_db_service.get_by_username(username)
    password_db_service = PasswordService()
    return password_db_service.verify(password, user.hashed_password)


async def _get_token_data(token):
    payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
        raise CredentialsException
    token_data = TokenData(username=username)

    return token_data
