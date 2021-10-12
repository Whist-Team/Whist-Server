"""User authentication."""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from whist.server.services.authentication import create_access_token

router = APIRouter(prefix='/user/auth')


@router.post('/')
def auth(request: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user for password.
    :param request: Must contain a dict with keys 'username' and 'password'.
    See 'OAuth2PasswordRequestForm'
    :return: the access token or 422 for insufficient request.
    """
    token_request = {'sub': request.username}
    token = create_access_token(token_request)
    return {'token': token}
