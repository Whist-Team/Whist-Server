"""User authentication."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from whist.server.database.access_token import AccessToken
from whist.server.services.authentication import create_access_token, check_credentials
from whist.server.services.error import UserNotFoundError

router = APIRouter(prefix='/user/auth')


@router.post('', response_model=AccessToken)
async def auth(request: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user for password.
    :param request: Must contain a dict with keys 'username' and 'password'.
    See 'OAuth2PasswordRequestForm'
    :return: the access token or 422 for insufficient request.
    """
    username = request.username
    password = request.password

    try:
        if not await check_credentials(username, password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect password.',
                headers={'WWW-Authenticate': 'Bearer'})
    except UserNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Incorrect username',
            headers={'WWW-Authenticate': 'Bearer'}
        ) from error
    token_request = {'sub': username}
    token = create_access_token(token_request)
    return AccessToken(access_token=token, token_type='Bearer')  # nosec B106
