import os

import httpx
from fastapi import APIRouter

from whist_server.database.access_token import AccessToken
from whist_server.services.authentication import create_access_token

router = APIRouter(prefix='/oauth2/github')


@router.post('', response_model=AccessToken)
async def swap_token(code: str):
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_url = os.getenv('REDIRECT_URL')
    data = {'client_id': client_id, 'client_secret': client_secret, 'code': code,
            'redirect_url': redirect_url}
    response = httpx.post('https://github.com/login/oauth/access_token', data=data)
    auth_token = response.json()['access_token']

    response = httpx.get('https://api.github.com/user',
                         headers={'Authorization': f'token {auth_token}'})
    username = response.json()['login']
    token_request = {'sub': username}
    token = create_access_token(token_request)
    return AccessToken(access_token=token, token_type='Bearer')  # nosec B106
