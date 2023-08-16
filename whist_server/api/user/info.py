"""Routes for user information."""
from fastapi import APIRouter, Security
from whist_core.user.player import Player

from whist_server.database.user import UserInDb
from whist_server.services.authentication import get_current_user

router = APIRouter(prefix='/user')


@router.get('/info')
def user_info(user: UserInDb = Security(get_current_user)) -> Player:
    """
    Returns the user information of the current user.
    :param user: the currently logged in user.
    """
    return user
