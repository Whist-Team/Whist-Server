"""Route of /room/game"""
from fastapi import APIRouter, BackgroundTasks, Depends, Security, status
from whist_core.game.errors import HandNotDoneError, HandDoneError
from whist_core.game.warnings import TrickNotDoneWarning

from whist_server.api.util import create_http_error
from whist_server.database.room import RoomInDb
from whist_server.database.user import UserInDb
from whist_server.services.authentication import get_current_user
from whist_server.services.channel_service import ChannelService
from whist_server.services.room_db_service import RoomDatabaseService
from whist_server.web_socket.events.event import NextHandEvent, NextTrickEvent

router = APIRouter(prefix='/room')


@router.post('/next_hand/{room_id}', status_code=200)
def next_hand(room_id: str, background_tasks: BackgroundTasks,
              user: UserInDb = Security(get_current_user),
              channel_service: ChannelService = Depends(ChannelService),
              room_service=Depends(RoomDatabaseService)) -> dict:
    """
    Request to start the next hand.
    :param room_id: at which table the card is requested to be played
    :param background_tasks: asynchronous handler
    :param user: requesting the next hand
    :param channel_service: Injection of the websocket channel manager.
    :param room_service: Injection of the room database service. Requires to interact with the
    database.
    :return: Status: 'Success' if next hand is created else raises error.
    """
    room: RoomInDb = room_service.get(room_id)
    if user not in room.players:
        message = f'Player: {user} has not joined {room}, yet.'
        raise create_http_error(message, status.HTTP_403_FORBIDDEN)
    try:
        _ = room.next_hand()
        room_service.save(room)
        background_tasks.add_task(channel_service.notify(room_id, NextHandEvent()))
    except HandNotDoneError as ready_error:
        message = 'The hand is not done yet.'
        raise create_http_error(message, status.HTTP_400_BAD_REQUEST) from ready_error
    return {'status': 'Success'}


@router.post('/next_trick/{room_id}', status_code=200)
def next_trick(room_id: str, background_tasks: BackgroundTasks,
               user: UserInDb = Security(get_current_user),
               channel_service: ChannelService = Depends(ChannelService),
               room_service=Depends(RoomDatabaseService)) -> dict:
    """
    Request to start the next trick.
    :param room_id: at which table the card is requested to be played
    :param background_tasks: asynchronous handler
    :param user: for which the hand is requested
    :param channel_service: Injection of the websocket channel manager.
    :param room_service: Injection of the room database service. Requires to interact with the
    database.
    :return: Status: 'Success' if next hand is created else raises error.
    """
    room: RoomInDb = room_service.get(room_id)
    if user not in room.players:
        message = f'Player: {user} has not joined {room}, yet.'
        raise create_http_error(message, status.HTTP_403_FORBIDDEN)
    try:
        _ = room.next_trick()
        room_service.save(room)
        background_tasks.add_task(channel_service.notify(room_id, NextTrickEvent()))
    except TrickNotDoneWarning as trick_not_done_warning:
        message = 'The trick is not done yet.'
        raise create_http_error(message, status.HTTP_400_BAD_REQUEST) from trick_not_done_warning
    except HandDoneError as hand_error:
        message = 'The hand is already done.'
        raise create_http_error(message, status.HTTP_400_BAD_REQUEST) from hand_error

    return {'status': 'Success'}
