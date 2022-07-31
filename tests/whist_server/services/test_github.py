from unittest.mock import patch, MagicMock

import pytest

from whist_server.services.github_service import GitHubAPIService


@pytest.mark.asyncio
async def test_token():
    service = GitHubAPIService()
    expected_token = 'fgh'
    with patch('httpx.post',
               MagicMock(return_value=MagicMock(
                   json=MagicMock(return_value={'access_token': expected_token})))):
        token = await service.get_github_token('cde')
    assert expected_token == token
