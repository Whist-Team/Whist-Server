"""'/' api"""

from fastapi import APIRouter

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
