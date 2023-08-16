"""Route to interaction with a table."""

from fastapi import APIRouter, BackgroundTasks, Depends, Security, status
from whist_core.error.table_error import PlayerNotJoinedError, TableNotReadyError

from whist_server.api.util import create_http_error
from whist_server.database.error import PlayerNotCreatorError
from whist_server.database.room import RoomInDb
from whist_server.database.user import UserInDb
from whist_server.services.authentication import get_current_user
from whist_server.services.channel_service import ChannelService
from whist_server.services.error import RoomNotFoundError
from whist_server.services.error import UserNotReadyError
from whist_server.services.room_db_service import RoomDatabaseService
from whist_server.services.splunk_service import SplunkService, SplunkEvent
from whist_server.web_socket.events.event import RoomStartedEvent

router = APIRouter(prefix='/room')


# Most of them are injections.
# pylint: disable=too-many-arguments
@router.post('/action/start/{room_id}', status_code=200)
def start_room(room_id: str, background_tasks: BackgroundTasks,
               user: UserInDb = Security(get_current_user),
               room_service=Depends(RoomDatabaseService),
               channel_service: ChannelService = Depends(ChannelService),
               splunk_service: SplunkService = Depends(SplunkService)) -> dict:
    """
    Allows the creator of the table to start it.
    :param room_id: unique identifier of the room
    :param background_tasks: asynchronous handler
    :param user: Required to identify if the user is the creator.
    :param room_service: Injection of the room database service. Requires to interact with the
    database.
    :param channel_service: Injection of the websocket channel manager.
    :param splunk_service: Injection of the Splunk Service.
    :return: dictionary containing the status of whether the table has been started or not.
    Raises 403 exception if the user has not the appropriate privileges.
    """
    room: RoomInDb = room_service.get(room_id)

    try:
        room.start(user)
        room.current_rubber.current_game().next_hand()
        room_service.save(room)
        if splunk_service.available:
            event = SplunkEvent(f'Room: {room.room_name}', source='Whist Server',
                                source_type='Room Started')

            splunk_service.write_event(event)
        background_tasks.add_task(channel_service.notify, room_id, RoomStartedEvent())
    except PlayerNotCreatorError as start_exception:
        message = 'Player has not administrator rights at this table.'
        raise create_http_error(message, status.HTTP_403_FORBIDDEN) from start_exception
    except TableNotReadyError as ready_error:
        message = 'At least one player is not ready and therefore the table cannot be started'
        raise create_http_error(message, status.HTTP_400_BAD_REQUEST) from ready_error

    return {'status': 'started'}


@router.post('/action/ready/{room_id}', status_code=200)
def ready_player(room_id: str, user: UserInDb = Security(get_current_user),
                 room_service=Depends(RoomDatabaseService)) -> dict:
    """
    A player can mark theyself to be ready.
    :param room_id: unique identifier of the room
    :param user: Required to identify the user.
    :param room_service: Injection of the room database service. Requires to interact with the
    database.
    :return: dictionary containing the status of whether the action was successful.
    Raises 403 exception if the user has not be joined yet.
    """
    room = room_service.get(room_id)

    try:
        room.ready_player(user)
        room_service.save(room)
    except PlayerNotJoinedError as ready_error:
        message = 'Player has not joined the table yet.'
        raise create_http_error(message, status.HTTP_403_FORBIDDEN) from ready_error
    return {'status': f'{user.username} is ready'}


@router.post('/action/unready/{room_id}', status_code=200)
def unready_player(room_id: str, user: UserInDb = Security(get_current_user),
                   room_service=Depends(RoomDatabaseService)) -> dict:
    """
    A player can mark themself to be unready.
    :param room_id: unique identifier of the room
    :param user: Required to identify the user.
    :param room_service: Injection of the room database service. Requires to interact with the
    database.
    :return: dictionary containing the status of whether the action was successful.
    Raises 403 exception if the user has not be joined yet.
    Raises 404 exception if room_id is not found
    Raises 400 exception if player is not ready
    """
    room = room_service.get(room_id)

    try:
        room.unready_player(user)
        room_service.save(room)
    except PlayerNotJoinedError as join_error:
        message = 'Player not joined yet.'
        raise create_http_error(message, status.HTTP_403_FORBIDDEN) from join_error
    except RoomNotFoundError as room_error:
        message = 'Room id not found'
        raise create_http_error(message, status.HTTP_404_NOT_FOUND) from room_error
    except UserNotReadyError as ready_error:
        message = 'Player not ready'
        raise create_http_error(message, status.HTTP_400_BAD_REQUEST) from ready_error
    return {'status': f'{user.username} is unready'}
