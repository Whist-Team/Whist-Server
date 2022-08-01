"""OAuth2 service for GitHub"""
import os

import httpx


class GitHubAPIService:
    """
    Singleton service that provides authentication with GitHub.
    """
    _instance = None
    _client_id = None
    _client_secret = None
    _redirect_url = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GitHubAPIService, cls).__new__(cls)
            cls._client_id = os.getenv('GITHUB_CLIENT_ID')
            cls._client_secret = os.getenv('GITHUB_CLIENT_SECRET')
            cls._redirect_url = os.getenv('GITHUB_REDIRECT_URL')
        return cls._instance

    @classmethod
    async def get_github_token(cls, code: str) -> str:
        """
        Retrieves the access token from GitHub.
        :param code: temporary code which needs to be provides by the client
        :return: access token
        """
        data = {'client_id': cls._client_id, 'client_secret': cls._client_secret, 'code': code,
                'redirect_url': cls._redirect_url}
        response = httpx.post('https://github.com/login/oauth/access_token', data=data)
        auth_token = response.json()['access_token']
        return auth_token

    @classmethod
    async def get_github_username(cls, auth_token: str) -> str:
        """
        Retrieves the GitHub's username.
        :param auth_token: the access token to GitHub.
        :return: username as string
        """
        response = httpx.get('https://api.github.com/user',
                             headers={'Authorization': f'token {auth_token}'})
        username = response.json()['login']
        return username
