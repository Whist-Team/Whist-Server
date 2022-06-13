from fastapi import APIRouter, Depends, WebSocket

from whist.server.services.authentication import get_current_user
from whist.server.services.error import GameNotFoundError
from whist.server.services.game_db_service import GameDatabaseService
from whist.server.web_socket.subscriber import Subscriber

router = APIRouter()


@router.websocket('/ping')
async def ping(ws: WebSocket):
    await ws.accept()
    await ws.send_text('pong')


@router.websocket('/room/{room_id}')
async def websocket(websocket: WebSocket, room_id: str,
                    game_service: GameDatabaseService = Depends(GameDatabaseService)):
    await websocket.accept()
    try:
        token = await websocket.receive_json()
        _ = get_current_user(token['token'])
        subscriber = Subscriber(websocket)
        room = game_service.get(room_id)
        room.side_channel.attach(subscriber)
        await websocket.send_text('200')
    except GameNotFoundError:
        await websocket.send_text('Game not found')
        await websocket.close()
