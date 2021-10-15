"""Route of /game/creation"""
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Security

from whist.server.database.game import GameInDb
from whist.server.database.user import User
from whist.server.services.authentication import get_current_user
from whist.server.services.game_db_service import GameDatabaseService
from whist.server.services.password import PasswordService

router = APIRouter(prefix='/game')


@router.post('/create', status_code=200)
def create_game(request: Dict[str, str], user: User=Security(get_current_user)):
    """
    Creates a new game of whist.
    :param request: Must contain a 'game_name'. 'password' is optional.
    :return: the ID of the game instance.
    """
    pwd_service = PasswordService()
    pwd_hash = _get_password(pwd_service, request)
    game_name = _get_game_name(request)

    game = GameInDb(game_name=game_name,
                    password=pwd_hash,
                    creator=str(user.id))
    game_db_service = GameDatabaseService()
    game_id = game_db_service.add(game)
    return {'game_id': game_id}


def _get_game_name(request):
    try:
        game_name = request['game_name']
    except KeyError as key_error:
        raise HTTPException(status_code=400, detail='"game_name" is required.') from key_error
    return game_name


def _get_password(pwd_service, request):
    try:
        password = request['password']
        pwd_hash = pwd_service.hash(password)
    except KeyError:
        pwd_hash = None
    return pwd_hash
