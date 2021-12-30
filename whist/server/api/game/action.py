"""Route to interaction with a table."""
from fastapi import APIRouter, Security, HTTPException, status
from whist.core.error.table_error import PlayerNotJoinedError, TableNotReadyError
from whist.core.user.player import Player

from whist.server.database.error import PlayerNotCreatorError
from whist.server.services.authentication import get_current_user
from whist.server.services.game_db_service import GameDatabaseService

router = APIRouter(prefix='/game')


@router.post('/action/start/{game_id}', status_code=200)
def start_game(game_id: str, user: Player = Security(get_current_user)) -> dict:
    """
    Allows the creator of the table to start it.
    :param game_id: unique identifier of the game
    :param user: Required to identify if the user is the creator.
    :return: dictionary containing the status of whether the table has been started or not.
    Raises 403 exception if the user has not the appropriate privileges.
    """
    game_service = GameDatabaseService()
    game = game_service.get(game_id)

    try:
        if game.start(user):
            return {'status': 'started'}
    except PlayerNotCreatorError as start_exception:
        message = 'Player has not administrator rights at this table.'
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
            headers={"WWW-Authenticate": "Basic"},
        ) from start_exception
    except TableNotReadyError as ready_error:
        message = 'At least one player is not ready and therefore the table cannot be started'
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
            headers={"WWW-Authenticate": "Basic"},
        ) from ready_error
    return {'status': 'not started'}


@router.post('/action/ready/{game_id}', status_code=200)
def ready_player(game_id: str, user: Player = Security(get_current_user)) -> dict:
    """
    A player can mark theyself to be ready.
    :param game_id: unique identifier of the game
    :param user: Required to identify the user.
    :return: dictionary containing the status of whether the action was successful.
    Raises 403 exception if the user has not be joined yet.
    """
    game_service = GameDatabaseService()
    game = game_service.get(game_id)

    try:
        game.ready_player(user)
        game_service.save(game)
    except PlayerNotJoinedError as ready_error:
        message = 'Player has not joined the table yet.'
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
            headers={"WWW-Authenticate": "Basic"},
        ) from ready_error
    return {'status': f'{user.username} is ready'}
