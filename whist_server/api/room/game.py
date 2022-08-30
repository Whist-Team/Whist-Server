from fastapi import APIRouter, BackgroundTasks, Depends

from whist_server.database.room import RoomInDb
from whist_server.services.channel_service import ChannelService
from whist_server.services.room_db_service import RoomDatabaseService
from whist_server.web_socket.events.event import NextHandEvent

router = APIRouter(prefix='/room')


@router.post('/next_hand/{room_id}', status_code=200)
def next_hand(room_id: str, background_tasks: BackgroundTasks,
              channel_service: ChannelService = Depends(ChannelService),
              room_service=Depends(RoomDatabaseService)) -> dict:
    """
    Request to start the next hand.
    :param room_id: at which table the card is requested to be played
    :param background_tasks: asynchronous handler
    :param channel_service: Injection of the websocket channel manager.
    :param room_service: Injection of the room database service. Requires to interact with the
    database.
    :return:Status: 'Success' or 'Failed'
    """
    room: RoomInDb = room_service.get(room_id)

    room.next_hand()
    room_service.save(room)
    background_tasks.add_task(channel_service.notify(room_id, NextHandEvent()))
    return {'status': 'Success'}
