"""Route of /room/creation"""
from typing import Optional

from fastapi import APIRouter, Depends, Security
from pydantic import BaseModel
from whist_core.error.table_error import TableSettingsError

from whist_server.api.util import create_http_error
from whist_server.database.user import UserInDb
from whist_server.services.authentication import get_current_user
from whist_server.services.channel_service import ChannelService
from whist_server.services.password import PasswordService
from whist_server.services.room_db_service import RoomDatabaseService
from whist_server.services.splunk_service import SplunkEvent, SplunkService
from whist_server.web_socket.side_channel import SideChannel

router = APIRouter(prefix='/room')


class CreateRoomArgs(BaseModel):
    """
    JSON body for creating room
    """
    room_name: str
    password: Optional[str] = None
    min_player: Optional[int] = None
    max_player: Optional[int] = None


# Most of them are injections.
# pylint: disable=too-many-arguments
@router.post('/create', status_code=200)
def create_game(request: CreateRoomArgs, user: UserInDb = Security(get_current_user),
                room_service=Depends(RoomDatabaseService), pwd_service=Depends(PasswordService),
                channel_service: ChannelService = Depends(ChannelService),
                splunk_service: SplunkService = Depends(SplunkService)):
    """
    Creates a new room of whist with the given name 'room_name' and optional password 'password'.
    The optional 'min_player' parameter controls how many people are required to start a room.
    The optional 'max_player' parameter controls how many people are allowed in a room.
    :param request: Must contain a 'room_name'. 'password', 'min_player', 'max_player' are optional.
    :param user: that created the room session.
    :param room_service: service to handle database interaction for rooms.
    :param pwd_service: service to handle password requests.
    :param channel_service: Injection of the websocket channel manager.
    :param splunk_service: Injection of the Splunk Service.
    :return: the ID of the room instance.
    """
    hashed_password = None if request.password is None else pwd_service.hash(request.password)
    try:
        room = room_service.create_with_pwd(room_name=request.room_name, creator=user,
                                            hashed_password=hashed_password,
                                            min_player=request.min_player,
                                            max_player=request.max_player)
    except TableSettingsError as table_error:
        raise create_http_error('Table setting was not correct.', 400) from table_error
    room_id = room_service.add(room)
    if splunk_service.available:
        event = SplunkEvent(f'Room: {room.room_name}', source='Whist Server',
                            source_type='Room Created')

        splunk_service.write_event(event)
    channel = SideChannel()
    channel_service.add(room_id, channel)
    return {'room_id': room_id}
