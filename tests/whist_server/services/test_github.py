from unittest.mock import patch, MagicMock

import pytest

from whist_server.services.error import GitHubAuthError
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
    route.assert_called_once_with('https://github.com/login/oauth/access_token', json=expected_data)


@pytest.mark.asyncio
async def test_device_token(setup_env):
    service = GitHubAPIService()
    expected_token = 'fgh'
    expected_data = {'client_id': CLIENT_ID, 'device_code': CODE,
                     'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'}
    with patch('httpx.post',
               MagicMock(return_value=MagicMock(
                   json=MagicMock(return_value={'access_token': expected_token})))) as route:
        token = await service.get_github_token_from_device_code(CODE)
    assert expected_token == token
    route.assert_called_once_with(headers={'Accept': 'application/json'},
                                  url='https://github.com/login/oauth/access_token',
                                  json=expected_data)


@pytest.mark.asyncio
async def test_device_token_error(setup_env):
    service = GitHubAPIService()
    expected_data = {'client_id': CLIENT_ID, 'device_code': CODE,
                     'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'}
    with patch('httpx.post',
               MagicMock(return_value=MagicMock(
                   json=MagicMock(return_value={'error': 'test_error', 'error_description':
                       'test', 'error_uri': '/error'})))) \
            as route:
        with pytest.raises(GitHubAuthError):
            _ = await service.get_github_token_from_device_code(CODE)
    route.assert_called_once_with(headers={'Accept': 'application/json'},
                                  url='https://github.com/login/oauth/access_token',
                                  json=expected_data)

@pytest.mark.asyncio
async def test_username():
    service = GitHubAPIService()
    expected_username = 'fgh'
    token = 'token'
    with patch('httpx.get',
               MagicMock(return_value=MagicMock(
                   json=MagicMock(return_value={'login': expected_username})))) as route:
        username = await service.get_github_username(token)
    assert expected_username == username
    route.assert_called_once_with('https://api.github.com/user',
                                  headers={'Authorization': f'token {token}'})

@pytest.mark.asyncio
async def test_username():
    service = GitHubAPIService()
    expected_id = 'fgh'
    token = 'token'
    with patch('httpx.get',
               MagicMock(return_value=MagicMock(
                   json=MagicMock(return_value={'id': expected_id})))) as route:
        user_id = await service.get_github_id(token)
    assert expected_id == user_id
    route.assert_called_once_with('https://api.github.com/user',
                                  headers={'Authorization': f'token {token}'})
