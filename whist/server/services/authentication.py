from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from whist.server.const import SECRET_KEY, ALGORITHM
from whist.server.database.token import TokenData
from whist.server.database.user import User
from whist.server.services.error import CredentialsException
from whist.server.services.user_db_service import UserDatabaseService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates an access token for an user.
    :param data: Expects a dictionary with with key 'sub' and an username as value.
    :param expires_delta: The amount of time until this token shall expire.
    :return: token as a str
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Retrieves the user from a token.
    :param token: access token
    :return: DO of User
    """
    token_data = await _get_token_data(token)
    user_db_service = UserDatabaseService()
    user = user_db_service.get_by_name(token_data.username)
    if user is None:
        raise CredentialsException()
    return user.to_user()


async def _get_token_data(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsException()
    return token_data
