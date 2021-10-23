from typing import Dict

from fastapi import APIRouter, Security

from whist.server.database.user import User
from whist.server.services.authentication import get_current_user

router = APIRouter(prefix='/game')


@router.post('/join/{game_id}', status_code=200)
def join_game(request: Dict[str, str], user: User = Security(get_current_user)):
    """
    User requests to join a game.
    :param request: must contain the key 'password'
    :param user: that tries to join the game. Must be authenticated.
    :return: the status of the join request. 'joined' for successful join
    """

    return {'status': 'joined'}
