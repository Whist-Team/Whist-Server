"""Collection of general game information getter."""
from fastapi import APIRouter, Depends, HTTPException, Security, status
from whist.core.user.player import Player

from whist.server.database.game import GameInDb
from whist.server.services.authentication import get_current_user
from whist.server.services.error import GameNotFoundError
from whist.server.services.game_db_service import GameDatabaseService

router = APIRouter(prefix='/game')


@router.get('/info/ids', status_code=200, response_model=dict[str, list[str]])
def all_games(game_service=Depends(GameDatabaseService),
              _: Player = Security(get_current_user)) -> dict[str, list[str]]:
    """
    Returns all game id.
    :param game_service: Dependency injection of the game service
    :param _: not required for logic, but authentication
    :return: a list of all game ids as strings.
    """
    rooms = game_service.all()
    return {'games': [str(room.id) for room in rooms]}


@router.get('/info/id/{game_name}', status_code=200, response_model=dict[str, str])
def game_id_from_name(game_name: str, game_service=Depends(GameDatabaseService),
                      user: Player = Security(get_current_user)) -> dict[str, str]:
    """
    Returns the game id for a given game name. Basically it transforms human-readable data to
    computer data.
    :param game_name: the human-readable game name
    :param game_service: Dependency injection of the game service
    :param user: not required for logic, but authentication
    :return: dictionary containing the field 'id' with the game id as value.If there is no game
    with that name in the DB it will return GameNotFoundError.
    """
    try:
        room: GameInDb = game_service.get_by_name(game_name)
        if not room.has_joined(user):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='User has not access.',
                                headers={"WWW-Authenticate": "Bearer"},
                                )
    except GameNotFoundError as not_found:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Game not found with name: {game_name}',
                            headers={"WWW-Authenticate": "Bearer"}, ) from not_found
    return {'id': str(room.id)}
