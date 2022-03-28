"""Collection of general game information getter."""
from fastapi import APIRouter, Depends, HTTPException, status

from whist.server.database.game import GameInDb
from whist.server.services.error import GameNotFoundError
from whist.server.services.game_db_service import GameDatabaseService

router = APIRouter(prefix='/game')


@router.get('/info/id/{game_name}', status_code=200, response_model=dict[str, str])
def game_id_from_name(game_name: str, game_service=Depends(GameDatabaseService)) -> dict[str, str]:
    """
    Returns the game id for a given game name. Basically it transforms human-readable data to
    computer data.
    :param game_name: the human-readable game name
    :param game_service: Dependency injection of the game service
    :return: dictionary containing the field 'id' with the game id as value.If there is no game
    with that name in the DB it will return GameNotFoundError.
    """
    try:
        room: GameInDb = game_service.get_by_name(game_name)
    except GameNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Game not found with name: {game_name}',
                            headers={"WWW-Authenticate": "Basic"}, )
    return {'id': str(room.id)}
