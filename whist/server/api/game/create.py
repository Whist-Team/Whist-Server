"""Route of /game/creation"""
from typing import Optional

from fastapi import APIRouter, Depends, Security
from pydantic import BaseModel
from whist.core.user.player import Player

from whist.server.services.authentication import get_current_user
from whist.server.services.channel_service import ChannelService
from whist.server.services.game_db_service import GameDatabaseService
from whist.server.services.password import PasswordService
from whist.server.web_socket.side_channel import SideChannel

router = APIRouter(prefix='/game')


class CreateGameArgs(BaseModel):
    """
    JSON body for creating game
    """
    game_name: str
    password: Optional[str] = None
    min_player: Optional[int] = None
    max_player: Optional[int] = None


@router.post('/create', status_code=200)
def create_game(request: CreateGameArgs, user: Player = Security(get_current_user),
                game_service=Depends(GameDatabaseService), pwd_service=Depends(PasswordService),
                channel_service: ChannelService = Depends(ChannelService)):
    """
    Creates a new game of whist with the given name 'game_name' and optional password 'password'.
    The optional 'min_player' parameter controls how many people are required to start a game.
    The optional 'max_player' parameter controls how many people are allowed in a game.
    :param request: Must contain a 'game_name'. 'password', 'min_player', 'max_player' are optional.
    :param user: that created the game session.
    :param game_service: service to handle database interaction for games.
    :param pwd_service: service to handle password requests.
    :param channel_service: Injection of the websocket channel manager.
    :return: the ID of the game instance.
    """
    hashed_password = None if request.password is None else pwd_service.hash(request.password)
    game = game_service.create_with_pwd(game_name=request.game_name, creator=user,
                                        hashed_password=hashed_password,
                                        min_player=request.min_player,
                                        max_player=request.max_player)
    game_id = game_service.add(game)
    channel = SideChannel()
    channel_service.add(game_id, channel)
    return {'game_id': game_id}
