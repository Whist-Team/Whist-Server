"""Route of /room/creation"""
from typing import Optional

from fastapi import APIRouter, Depends, Security
from pydantic import BaseModel
from whist.core.user.player import Player

from whist.server.services.authentication import get_current_user
from whist.server.services.channel_service import ChannelService
from whist.server.services.password import PasswordService
from whist.server.services.room_db_service import RoomDatabaseService
from whist.server.web_socket.side_channel import SideChannel

router = APIRouter(prefix='/room')


class CreateRoomArgs(BaseModel):
    """
    JSON body for creating room
    """
    room_name: str
    password: Optional[str] = None
    min_player: Optional[int] = None
    max_player: Optional[int] = None


@router.post('/create', status_code=200)
def create_game(request: CreateRoomArgs, user: Player = Security(get_current_user),
                room_service=Depends(RoomDatabaseService), pwd_service=Depends(PasswordService),
                channel_service: ChannelService = Depends(ChannelService)):
    """
    Creates a new room of whist with the given name 'room_name' and optional password 'password'.
    The optional 'min_player' parameter controls how many people are required to start a room.
    The optional 'max_player' parameter controls how many people are allowed in a room.
    :param request: Must contain a 'room_name'. 'password', 'min_player', 'max_player' are optional.
    :param user: that created the room session.
    :param room_service: service to handle database interaction for rooms.
    :param pwd_service: service to handle password requests.
    :param channel_service: Injection of the websocket channel manager.
    :return: the ID of the room instance.
    """
    hashed_password = None if request.password is None else pwd_service.hash(request.password)
    room = room_service.create_with_pwd(room_name=request.room_name, creator=user,
                                        hashed_password=hashed_password,
                                        min_player=request.min_player,
                                        max_player=request.max_player)
    room_id = room_service.add(room)
    channel = SideChannel()
    channel_service.add(room_id, channel)
    return {'room_id': room_id}
