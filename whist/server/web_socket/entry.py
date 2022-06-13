"""Routes of the websocket communication."""
from fastapi import APIRouter, Depends, WebSocket
from whist.core.error.table_error import PlayerNotJoinedError

from whist.server.services.authentication import get_current_user
from whist.server.services.error import GameNotFoundError
from whist.server.services.game_db_service import GameDatabaseService
from whist.server.web_socket.subscriber import Subscriber

router = APIRouter()


@router.websocket('/ping')
async def ping(websocket: WebSocket):
    """
    Sends 'pong' to the client as response.
    :param websocket: communication end point of the client
    """
    await websocket.accept()
    await websocket.send_text('pong')


@router.websocket('/room/{room_id}')
async def subscribe_room(websocket: WebSocket, room_id: str,
                         game_service: GameDatabaseService = Depends(GameDatabaseService)):
    """
    Clients requests to subscribe to room's side channel.
    :param websocket: communication end point of the client
    :param room_id: ID of the room to which should be subscribed
    :param game_service: handles all request to the db regarding rooms.
    :return: Sends response to the websockets. No return.
    """
    await websocket.accept()
    try:
        token = await websocket.receive_json()
        player = get_current_user(token['token'])
        subscriber = Subscriber(websocket)
        room = game_service.get(room_id)
        _ = room.get_player(player)
        room.side_channel.attach(subscriber)
        await websocket.send_text('200')
    except GameNotFoundError:
        await websocket.send_text('Game not found')
        await websocket.close()
    except PlayerNotJoinedError:
        await websocket.send_text('User not joined')
        await websocket.close()
