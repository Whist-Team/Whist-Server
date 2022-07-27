import os

import httpx


class GitHubAPIService:
    _instance = None
    _client_id = None
    _client_secret = None
    _redirect_url = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GitHubAPIService, cls).__new__(cls)
            cls._client_id = os.getenv('CLIENT_ID')
            cls._client_secret = os.getenv('CLIENT_SECRET')
            cls._redirect_url = os.getenv('REDIRECT_URL')
        return cls._instance

    @classmethod
    async def _get_github_token(cls, code: str) -> str:
        data = {'client_id': cls._client_id, 'client_secret': cls._client_secret, 'code': code,
                'redirect_url': cls._redirect_url}
        response = httpx.post('https://github.com/login/oauth/access_token', data=data)
        auth_token = response.json()['access_token']
        return auth_token

    @classmethod
    async def _get_github_username(cls, auth_token: str) -> str:
        response = httpx.get('https://api.github.com/user',
                             headers={'Authorization': f'token {auth_token}'})
        username = response.json()['login']
        return username
