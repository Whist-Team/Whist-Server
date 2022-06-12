"""Route of /game/creation"""
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from whist.core.user.player import Player

from whist.server.services.authentication import get_current_user
from whist.server.services.game_db_service import GameDatabaseService
from whist.server.services.password import PasswordService

router = APIRouter(prefix='/game')


@router.post('/create', status_code=200)
def create_game(request: Dict[str, str], user: Player = Depends(get_current_user),
                game_service=Depends(GameDatabaseService), pwd_service=Depends(PasswordService)):
    """
    Creates a new game of whist.
    :param request: Must contain a 'game_name'. 'password' is optional.
    :param user: that created the game session.
    :param game_service: service to handle database interaction for games.
    :param pwd_service: service to handle password requests.
    :return: the ID of the game instance.
    """
    game_parameter = _set_game_parameter(request, user, pwd_service)
    game = game_service.create_with_pwd(**game_parameter)
    game_id = game_service.add(game)
    return {'game_id': game_id}


def _set_game_parameter(request, user, pwd_service: PasswordService):
    """
    Sets the maximum and minimum level for players to join game.
    :param request: Must contain a 'game_name'. 'password' is optional
    :param user: that created the game session.
    :param pwd_service: service to handle password requests.
    :return: the players in the game
    """
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
    """
    Checks to see if player is in the level range.
    :param request: Must contain a 'game_name'. 'password' is optional
    :param key: the player entering game
    """
    if key not in ['min_player', 'max_player']:
      raise KeyError(f'{key} is not a valid key for this operation.')
    if key in request:
      return int(request[key])
    return None


def _get_game_name(request):
    """
    Creates a game name.
    :param request: Must contain a 'game_name'. 'password' is optional
    :return: the game name instance
    """
    try:
      game_name = request['game_name']
    except KeyError as key_error:
      raise HTTPException(status_code=400, detail='"game_name" is required.') from key_error
    return game_name


def _get_password(pwd_service, request):
    """
    Creates a password for game.
    :param request: Must contain a 'game_name'. 'password' is optional
    :param pwd_service: service to handle password requests.
    :return: the password for game instance
    """
    try:
      password = request['password']
      pwd_hash = pwd_service.hash(password)
    except KeyError:
      pwd_hash = None
    return pwd_hash
