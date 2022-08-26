"""Token swap routes for authentication with GitHub"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from whist_server.database.access_token import AccessToken
from whist_server.database.user import UserInDb
from whist_server.services import authentication
from whist_server.services.error import UserNotFoundError
from whist_server.services.github_service import GitHubAPIService
from whist_server.services.user_db_service import UserDatabaseService

router = APIRouter(prefix='/oauth2/github')


class SwapTokenRequestData(BaseModel):
    """
    Data wrapper containing the temporary code provided by GitHub.
    """
    code: str


class SwapDeviceCodeRequestData(BaseModel):
    """
    Data wrapper containing the temporary code provided by GitHub.
    """
    device_code: str


@router.post('', response_model=AccessToken)
async def swap_token(data: SwapTokenRequestData, github_service=Depends(GitHubAPIService),
                     user_db_service=Depends(UserDatabaseService)):
    """
    Swaps the GitHub Auth Token for an Access Token.
    :param data: Wrapper containing a 'code' which is the temporary code provided by GitHub.
    :param github_service: API adapter service for GitHub.
    :param user_db_service: service to handle request to the database storing users.
    :return: Internal application Access Token.
    """
    auth_token = await github_service.get_github_token(data.code)
    gh_id = await github_service.get_github_id(auth_token)
    user = user_db_service.get_from_github(gh_id)
    token_request = {'sub': user.username}
    token = authentication.create_access_token(token_request)
    return AccessToken(access_token=token, token_type='Bearer')  # nosec B106


@router.post('/device', response_model=AccessToken)
async def device_code_swap(data: SwapDeviceCodeRequestData,
                           github_service=Depends(GitHubAPIService),
                           user_db_service=Depends(UserDatabaseService)):
    """
    Swaps the GitHub device code for an Access Token.
    :param data: Wrapper containing a 'code' which is the temporary code provided by GitHub.
    :param github_service: API adapter service for GitHub.
    :param user_db_service: service to handle request to the database storing users.
    :return: Internal application Access Token.
    """
    auth_token = await github_service.get_github_token_from_device_code(data.device_code)
    github_id = await github_service.get_github_id(auth_token)

    try:
        user = user_db_service.get_from_github(github_id)
    except UserNotFoundError:
        gh_username = await github_service.get_github_username(auth_token)
        user = UserInDb(github_id=github_id, github_username=gh_username, username=gh_username)
        _ = user_db_service.add(user)
    token_request = {'sub': user.username}
    token = authentication.create_access_token(token_request)
    return AccessToken(access_token=token, token_type='Bearer')  # nosec B106
