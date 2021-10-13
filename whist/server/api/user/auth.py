"""User authentication."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from whist.server.services.authentication import create_access_token, check_credentials

router = APIRouter(prefix='/user/auth')


@router.post('/')
async def auth(request: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user for password.
    :param request: Must contain a dict with keys 'username' and 'password'.
    See 'OAuth2PasswordRequestForm'
    :return: the access token or 422 for insufficient request.
    """
    username = request.username
    password = request.password

    if not await check_credentials(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password.',
            headers={'WWW-Authenticate': 'Basic'})
    token_request = {'sub': username}
    token = create_access_token(token_request)
    return {'token': token}
