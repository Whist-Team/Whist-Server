"""
Route to join a game.
"""
from typing import Dict

from fastapi import APIRouter, HTTPException, Security, status
from whist.core.user.player import Player

from whist.server.database.warning import PlayerAlreadyJoinedWarning
from whist.server.services.authentication import get_current_user
from whist.server.services.game_db_service import GameDatabaseService
from whist.server.services.password import PasswordService

router = APIRouter(prefix='/game')


@router.post('/join/{game_id}', status_code=200)
def join_game(game_id: str, request: Dict[str, str], user: Player = Security(get_current_user)):
    """
    User requests to join a game.
    :param game_id: unique identifier for a game
    :param request: must contain the key 'password'
    :param user: that tries to join the game. Must be authenticated.
    :return: the status of the join request. 'joined' for successful join
    """
    pwd_service = PasswordService()

    game_pwd = request['password']

    game_service = GameDatabaseService()
    game = game_service.get(game_id)

    if not pwd_service.verify(game_pwd, game.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong game password.",
            headers={"WWW-Authenticate": "Basic"},
        )
    try:
        game.join(user)
        game_service.save(game)
    except PlayerAlreadyJoinedWarning:
        return {'status': 'already joined'}
    return {'status': 'joined'}
