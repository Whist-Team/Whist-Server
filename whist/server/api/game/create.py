"""Route of /game/creation"""
from typing import Dict, Optional

from fastapi import APIRouter, HTTPException, Security
from whist.core.user.player import Player

from whist.server.database.game import GameInDb
from whist.server.services.authentication import get_current_user
from whist.server.services.game_db_service import GameDatabaseService
from whist.server.services.password import PasswordService

router = APIRouter(prefix='/game')


@router.post('/create', status_code=200)
def create_game(request: Dict[str, str], user: Player = Security(get_current_user)):
    """
    Creates a new game of whist.
    :param request: Must contain a 'game_name'. 'password' is optional.
    :param user: that created the game session.
    :return: the ID of the game instance.
    """
    game_parameter = _set_game_parameter(request, user)
    game = GameInDb.create_with_pwd(**game_parameter)
    game_db_service = GameDatabaseService()
    game_id = game_db_service.add(game)
    return {'game_id': game_id}


def _set_game_parameter(request, user):
    pwd_service = PasswordService()
    pwd_hash = _get_password(pwd_service, request)
    game_name = _get_game_name(request)
    game_parameter = dict(game_name=game_name,
                          hashed_password=pwd_hash,
                          creator=user)
    min_player = _get_amount_player(request, 'min_player')
    if min_player is not None:
        game_parameter.update({'min_player': min_player})
    max_player = _get_amount_player(request, 'max_player')
    if max_player is not None:
        game_parameter.update({'max_player': max_player})
    return game_parameter


def _get_amount_player(request, key) -> Optional[int]:
    if key not in ['min_player', 'max_player']:
        raise KeyError(f'{key} is not a valid key for this operation.')
    if key in request:
        return int(request[key])
    return None


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
