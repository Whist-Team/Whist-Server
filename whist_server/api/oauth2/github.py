import os

import httpx
from fastapi import APIRouter

from whist_server.database.access_token import AccessToken
from whist_server.services.authentication import create_access_token

router = APIRouter(prefix='/oauth2/github')


@router.post('', response_model=AccessToken)
async def swap_token(code: str):
    """
    Swaps the GitHub Auth Token for an Access Token.
    :param code: Temporary code provided by GitHub.
    :return: Internal application Access Token.
    """
    auth_token = await _get_github_token(code)
    username = await _get_github_username(auth_token)
    token_request = {'sub': username}
    token = create_access_token(token_request)
    return AccessToken(access_token=token, token_type='Bearer')  # nosec B106


async def _get_github_token(code: str) -> str:
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_url = os.getenv('REDIRECT_URL')
    data = {'client_id': client_id, 'client_secret': client_secret, 'code': code,
            'redirect_url': redirect_url}
    response = httpx.post('https://github.com/login/oauth/access_token', data=data)
    auth_token = response.json()['access_token']
    return auth_token


async def _get_github_username(auth_token: str) -> str:
    response = httpx.get('https://api.github.com/user',
                         headers={'Authorization': f'token {auth_token}'})
    username = response.json()['login']
    return username
