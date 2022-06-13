from fastapi import APIRouter, Depends, Query, WebSocket
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

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
async def websocket(websocket: WebSocket, room_id: str, token: str = Query(...),
                    Authorize: AuthJWT = Depends(),
                    game_service: GameDatabaseService = Depends(GameDatabaseService)):
    await websocket.accept()
    try:
        Authorize.jwt_required("websocket", token=token)
        _ = get_current_user(token)
        subscriber = Subscriber(websocket)
        room = game_service.get(room_id)
        room.side_channel.attach(subscriber)
    except AuthJWTException as err:
        await websocket.send_text(err.message)
        await websocket.close()
