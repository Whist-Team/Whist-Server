"""Route of /game/creation"""
from typing import Optional

from fastapi import APIRouter, Depends, Security, HTTPException
from pydantic import BaseModel
from whist.core.user.player import Player

from whist.server.services.authentication import get_current_user
from whist.server.services.game_db_service import GameDatabaseService
from whist.server.services.password import PasswordService

router = APIRouter(prefix='/game')


class CreateGameArgs(BaseModel):
    game_name: str
    password: Optional[str] = None
    min_player: Optional[int] = None
    max_player: Optional[int] = None


@router.post('/create', status_code=200)
def create_game(request: CreateGameArgs, user: Player = Security(get_current_user),
                game_service=Depends(GameDatabaseService), pwd_service=Depends(PasswordService)):
    """
    Creates a new game of whist.
    :param request: Must contain a 'game_name'. 'password' is optional.
    :param user: that created the game session.
    :param game_service: service to handle database interaction for games.
    :param pwd_service: service to handle password requests.
    :return: the ID of the game instance.
    """
    hashed_password = None if request.password is None else pwd_service.hash(request.password)
    game = game_service.create_with_pwd(game_name=request.game_name, creator=user,
                                        hashed_password=hashed_password,
                                        min_player=request.min_player,
                                        max_player=request.max_player)
    game_id = game_service.add(game)
    return {'game_id': game_id}
