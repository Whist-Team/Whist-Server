"""
Route to join a room.
"""
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Security, status, Depends
from pydantic import BaseModel

from whist_server.api.util import create_http_error
from whist_server.database.error import PlayerNotJoinedError
from whist_server.database.room import RoomInfo
from whist_server.database.user import UserInDb
from whist_server.database.warning import PlayerAlreadyJoinedWarning
from whist_server.services.authentication import get_current_user
from whist_server.services.channel_service import ChannelService
from whist_server.services.error import RoomNotFoundError
from whist_server.services.password import PasswordService
from whist_server.services.room_db_service import RoomDatabaseService
from whist_server.web_socket.events.event import PlayerJoinedEvent, PlayerLeftEvent

router = APIRouter(prefix='/room')


class JoinRoomArgs(BaseModel):
    """
    JSON body for joining room
    """
    password: Optional[str] = None


# Most of them are injections.
# pylint: disable=too-many-arguments
@router.post('/join/{room_id}', status_code=200)
def join_game(room_id: str, request: JoinRoomArgs, background_tasks: BackgroundTasks,
              user: UserInDb = Security(get_current_user),
              pwd_service=Depends(PasswordService), room_service=Depends(RoomDatabaseService),
              channel_service: ChannelService = Depends(ChannelService)):
    """
    User requests to join a room.
    :param room_id: unique identifier for a room
    :param request: may contain the key 'password'
    :param background_tasks: asynchronous handler
    :param user: that tries to join the room. Must be authenticated.
    :param pwd_service: Injection of the password service. Required to create and check passwords.
    :param room_service: Injection of the room database service. Requires to interact with the
    database.
    :param channel_service: Injection of the websocket channel manager.
    :return: the status of the join request. 'joined' for successful join
    """
    room = room_service.get(room_id)
    if room.hashed_password is not None and (
            request.password is None or not pwd_service.verify(request.password,
                                                               room.hashed_password)):
        message = "Wrong room password."
        raise create_http_error(message, status.HTTP_401_UNAUTHORIZED)
    try:
        room.join(user)
        room_service.save(room)
        background_tasks.add_task(channel_service.notify, room_id,
                                  PlayerJoinedEvent(player=user.to_player()))
    except PlayerAlreadyJoinedWarning:
        return {'status': 'already joined'}
    return {'status': 'joined'}


# Most of them are injections.
# pylint: disable=too-many-arguments
@router.post('/leave/{room_id}', status_code=200)
def leave_game(room_id: str, background_tasks: BackgroundTasks,
               user: UserInDb = Security(get_current_user),
               room_service=Depends(RoomDatabaseService),
               channel_service: ChannelService = Depends(ChannelService)):
    """
    User requests to leave a room.
    :param room_id: unique identifier for a room
    :param background_tasks: asynchronous handler
    :param user: that tries to leave the room. Must be authenticated.
    :param room_service: Injection of the room database service. Requires to interact with the
    database.
    :param channel_service: Injection of the websocket channel manager.
    :return: the status of the leave request. 'left' for successful join
    """
    room = room_service.get(room_id)

    try:
        room.leave(user)
        room_service.save(room)
        background_tasks.add_task(channel_service.notify, room_id,
                                  PlayerLeftEvent(player=user.to_player()))
    except PlayerNotJoinedError as joined_error:
        raise create_http_error('Player not joined', status.HTTP_403_FORBIDDEN) from joined_error
    return {'status': 'left'}


class ReconnectArguments(BaseModel):
    """
    Sets flags for extra response fields.
    """
    stack: bool = False


@router.post('/reconnect/', status_code=200)
def reconnect(args: ReconnectArguments = ReconnectArguments(stack=False),
              user: UserInDb = Security(get_current_user),
              room_service=Depends(RoomDatabaseService)):
    """
    Finds the room a player has joined.
    :param args: Request extra fields.
    :param user: requesting their room
    :param room_service: Injection of the room database service. Requires to interact with the
    database.
    :return: dictionary containing the room id and the status either 'joined' or 'not joined'.
    For the later no room id is sent.
    """
    try:
        room = room_service.get_by_user_id(user.id)
    except RoomNotFoundError:
        return {'status': 'not joined'}
    response = {'status': 'joined', 'room_id': str(room.id),
                'room_info': RoomInfo.from_room(room)}
    if args.stack:
        response.update({'stack': room.current_trick().stack})
    return response
