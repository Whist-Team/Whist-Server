"""Routes of the websocket communication."""
from fastapi import APIRouter, Depends, WebSocket
from whist.core.error.table_error import PlayerNotJoinedError

from whist.server.services.authentication import get_current_user
from whist.server.services.channel_service import ChannelService
from whist.server.services.error import GameNotFoundError
from whist.server.services.game_db_service import GameDatabaseService
from whist.server.services.user_db_service import UserDatabaseService
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
                         channel_service: ChannelService = Depends(ChannelService),
                         game_service: GameDatabaseService = Depends(GameDatabaseService),
                         user_service: UserDatabaseService = Depends(UserDatabaseService)):
    """
    Clients requests to subscribe to room's side channel.
    :param websocket: communication end point of the client. The body of the request must contain
    the bare string token.
    :param room_id: ID of the room to which should be subscribed
    :param channel_service: handles the websocket management.
    :param game_service: handles all request to the db regarding rooms.
    :param user_service: handles all request to the db regarding users.
    :return: Sends response to the websockets. No return.
    """
    await websocket.accept()
    try:
        token = await websocket.receive_text()
        player = await get_current_user(token, user_service)
        subscriber = Subscriber(websocket)
        room = game_service.get(room_id)
        if not room.has_joined(player):
            raise PlayerNotJoinedError()
        channel_service.attach(room_id, subscriber)
        await websocket.send_text('200')
    except GameNotFoundError:
        await websocket.close(reason='Game not found')
    except PlayerNotJoinedError:
        await websocket.close(reason='User not joined')
