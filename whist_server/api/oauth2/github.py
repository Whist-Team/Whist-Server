from fastapi import APIRouter, Depends

from whist_server.database.access_token import AccessToken
from whist_server.services.authentication import create_access_token
from whist_server.services.github_service import GitHubAPIService
from whist_server.services.user_db_service import UserDatabaseService

router = APIRouter(prefix='/oauth2/github')


@router.post('', response_model=AccessToken)
async def swap_token(code: str, github_service=Depends(GitHubAPIService),
                     user_db_service=Depends(UserDatabaseService)):
    """
    Swaps the GitHub Auth Token for an Access Token.
    :param code: Temporary code provided by GitHub.
    :param github_service: API adapter service for GitHub.
    :param user_db_service: service to handle request to the database storing users.
    :return: Internal application Access Token.
    """
    auth_token = await github_service.get_github_token(code)
    gh_username = await github_service.get_github_username(auth_token)
    user = user_db_service.get_from_github(gh_username)
    token_request = {'sub': user.username}
    token = create_access_token(token_request)
    return AccessToken(access_token=token, token_type='Bearer')  # nosec B106
