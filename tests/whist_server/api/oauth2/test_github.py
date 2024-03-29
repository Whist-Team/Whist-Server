from unittest import TestCase
from unittest.mock import MagicMock, patch, AsyncMock

from starlette.testclient import TestClient

from whist_server import app
from whist_server.database.access_token import AccessToken
from whist_server.services.error import UserNotFoundError
from whist_server.services.github_service import GitHubAPIService
from whist_server.services.user_db_service import UserDatabaseService


class GithubAuthTestCase(TestCase):
    def setUp(self) -> None:
        self.gh_service = AsyncMock(get_github_username=AsyncMock(return_value='test'),
                                    get_github_id=AsyncMock(return_value='123'))
        user_mock = MagicMock(username='test')
        self.user_service = AsyncMock(get_from_github=MagicMock(return_value=user_mock))
        app.dependency_overrides[GitHubAPIService] = lambda: self.gh_service
        app.dependency_overrides[UserDatabaseService] = lambda: self.user_service
        self.client = TestClient(app)
        self.app = app

    def test_swap(self):
        expected_token = AccessToken(access_token='abc', token_type='Bearer')
        with patch('whist_server.services.authentication.create_access_token',
                   MagicMock(return_value=expected_token.access_token)):
            response = self.client.post(url='/oauth2/github', json={'code': 'cde'})
        token = AccessToken(**response.json())
        self.assertEqual(expected_token, token)

    def test_device_swap(self):
        expected_token = AccessToken(access_token='abc', token_type='Bearer')
        with patch('whist_server.services.authentication.create_access_token',
                   MagicMock(return_value=expected_token.access_token)):
            response = self.client.post(url='/oauth2/github/device', json={'device_code': 'cde'})
        token = AccessToken(**response.json())
        self.assertEqual(expected_token, token)

    def test_device_swap_create_user(self):
        self.user_service.get_from_github = MagicMock(side_effect=UserNotFoundError)
        expected_token = AccessToken(access_token='abc', token_type='Bearer')
        with patch('whist_server.services.authentication.create_access_token',
                   MagicMock(return_value=expected_token.access_token)):
            response = self.client.post(url='/oauth2/github/device', json={'device_code': 'cde'})
        token = AccessToken(**response.json())
        self.assertEqual(expected_token, token)
