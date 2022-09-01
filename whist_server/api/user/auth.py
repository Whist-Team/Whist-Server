"""User authentication."""

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from whist_server.api.util import create_http_error
from whist_server.database.access_token import AccessToken
from whist_server.services import authentication
from whist_server.services.authentication import create_access_token
from whist_server.services.error import UserNotFoundError

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
        if not await authentication.check_credentials(username, password):
            raise create_http_error('Incorrect password', status.HTTP_401_UNAUTHORIZED)
    except UserNotFoundError as error:
        raise create_http_error('Incorrect username', status.HTTP_403_FORBIDDEN) from error
    token_request = {'sub': username}
    token = create_access_token(token_request)
    return AccessToken(access_token=token, token_type='Bearer')  # nosec B106
