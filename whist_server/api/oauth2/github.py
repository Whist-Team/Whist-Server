from fastapi import APIRouter, Depends

from whist_server.database.access_token import AccessToken
from whist_server.services.authentication import create_access_token
from whist_server.services.github_service import GitHubAPIService

router = APIRouter(prefix='/oauth2/github')


@router.post('', response_model=AccessToken)
async def swap_token(code: str, github_service=Depends(GitHubAPIService)):
    """
    Swaps the GitHub Auth Token for an Access Token.
    :param code: Temporary code provided by GitHub.
    :param github_service: API adapter service for GitHub.
    :return: Internal application Access Token.
    """
    auth_token = await github_service.get_github_token(code)
    username = await github_service.get_github_username(auth_token)
    token_request = {'sub': username}
    token = create_access_token(token_request)
    return AccessToken(access_token=token, token_type='Bearer')  # nosec B106
