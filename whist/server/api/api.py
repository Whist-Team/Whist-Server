"""'/' api"""
import os.path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from whist.server.services.game_info_db_service import GameInfoDatabaseService

router = APIRouter()


@router.get('/')
def read_root():
    """
    Index route of the server.
    :return: The game the server can host.
    """
    game_info_db_service = GameInfoDatabaseService()
    return {'info': game_info_db_service.get()}


@router.get('/favicon.ico')
async def favicon():
    """
    Returns the Favicon.
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '../../../static/ace-of-spades-icon-17.jpg')
    return FileResponse(path)
