"""Collection of general room information getter."""
from fastapi import APIRouter, Depends, Security, status

from whist_server.api.util import create_http_error
from whist_server.database.room import RoomInDb, RoomInfo
from whist_server.database.user import UserInDb
from whist_server.services.authentication import get_current_user
from whist_server.services.error import RoomNotFoundError
from whist_server.services.room_db_service import RoomDatabaseService

router = APIRouter(prefix='/room')


@router.get('/info/ids', status_code=200, response_model=dict[str, list[str]])
def all_rooms(room_service=Depends(RoomDatabaseService),
              _: UserInDb = Security(get_current_user)) -> dict[str, list[str]]:
    """
    Returns all room id.
    :param room_service: Dependency injection of the room service
    :param _: not required for logic, but authentication
    :return: a list of all room ids as strings.
    """
    rooms = room_service.all()
    return {'rooms': [str(room.id) for room in rooms]}


@router.get('/info/{room_id}', response_model=RoomInfo)
def room_info(room_id: str, room_service=Depends(RoomDatabaseService)) -> RoomInfo:
    """
    :param room_id:
    :param room_service: Dependency injection of the room service
    :return:
    """
    try:
        room = room_service.get(room_id)
    except RoomNotFoundError as not_found:
        message = f'Room not found with id: {room_id}'
        raise create_http_error(message, status.HTTP_400_BAD_REQUEST) from not_found
    return room.get_info()


@router.get('/info/id/{room_name}', status_code=200, response_model=dict[str, str])
def room_id_from_name(room_name: str, room_service=Depends(RoomDatabaseService),
                      user: UserInDb = Security(get_current_user)) -> dict[str, str]:
    """
    Returns the room id for a given room name. Basically it transforms human-readable data to
    computer data.
    :param room_name: the human-readable room name
    :param room_service: Dependency injection of the room service
    :param user: not required for logic, but authentication
    :return: dictionary containing the field 'id' with the room id as value.If there is no room
    with that name in the DB it will return RoomNotFoundError.
    """
    try:
        room: RoomInDb = room_service.get_by_name(room_name)
        if not room.has_joined(user):
            message = 'User has not access.'
            raise create_http_error(message, status.HTTP_403_FORBIDDEN)
    except RoomNotFoundError as not_found:
        message = f'Room not found with name: {room_name}'
        raise create_http_error(message, status.HTTP_400_BAD_REQUEST) from not_found
    return {'id': str(room.id)}
