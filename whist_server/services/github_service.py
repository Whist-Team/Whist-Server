"""OAuth2 service for GitHub"""
import os

import httpx

from whist_server.services.error import GitHubAuthError


class GitHubAPIService:
    """
    Singleton service that provides authentication with GitHub.
    """
    _instance = None
    _client_id = None
    _client_secret = None
    _redirect_url = None

    def __new__(cls):
        """Creates a new instance of this service singleton."""
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
        response = httpx.post('https://github.com/login/oauth/access_token', json=data)
        auth_token = response.json()['access_token']
        return auth_token

    @classmethod
    async def get_github_token_from_device_code(cls, code: str) -> str:
        """
        Retrieves the access token from GitHub.
        :param code: temporary code which needs to be provides by the client
        :return: access token
        """
        data = {'client_id': cls._client_id, 'device_code': code,
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'}
        response = httpx.post(headers={'Accept': 'application/json'},
                              url='https://github.com/login/oauth/access_token',
                              json=data)

        response_json: dict = response.json()
        if 'error' in response_json.keys():
            raise GitHubAuthError(**response_json)
        auth_token = response_json['access_token']
        return auth_token

    @classmethod
    async def get_github_id(cls, auth_token: str) -> str:
        """
        Retrieves the GitHub's user id.
        :param auth_token: the access token to GitHub.
        :return: GitHubs's user_id as string
        """
        response = httpx.get('https://api.github.com/user',
                             headers={'Authorization': f'token {auth_token}'})
        github_id = response.json()['id']
        return github_id

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
