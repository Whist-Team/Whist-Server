from unittest.mock import patch, MagicMock

import pytest

from whist_server.services.github_service import GitHubAPIService

CLIENT_ID = '1'
CLIENT_SECRET = 'secret'
CODE = 'code'
REDIRECT_URL = 'http://redirect'


@pytest.fixture
def setup_env(monkeypatch):
    monkeypatch.setenv('GITHUB_CLIENT_ID', CLIENT_ID)
    monkeypatch.setenv('GITHUB_CLIENT_SECRET', CLIENT_SECRET)
    monkeypatch.setenv('GITHUB_REDIRECT_URL', REDIRECT_URL)


@pytest.mark.asyncio
async def test_token(setup_env):
    service = GitHubAPIService()
    expected_token = 'fgh'
    expected_data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'code': CODE,
                     'redirect_url': REDIRECT_URL}
    with patch('httpx.post',
               MagicMock(return_value=MagicMock(
                   json=MagicMock(return_value={'access_token': expected_token})))) as route:
        token = await service.get_github_token(CODE)
    assert expected_token == token
    route.assert_called_once_with('https://github.com/login/oauth/access_token', data=expected_data)


@pytest.mark.asyncio
async def test_username():
    service = GitHubAPIService()
    expected_username = 'fgh'
    with patch('httpx.post',
               MagicMock(return_value=MagicMock(
                   json=MagicMock(return_value={'access_token': expected_username})))):
        token = await service.get_github_token('cde')
    assert expected_username == token
