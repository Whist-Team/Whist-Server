"""Route to interaction with a table."""
from typing import Optional

import logging

from fastapi import APIRouter, Depends, Security, HTTPException, status
from pydantic import BaseModel
from whist.core.error.table_error import PlayerNotJoinedError, TableNotReadyError
from whist.core.session.matcher import RandomMatcher, RoundRobinMatcher, Matcher
from whist.core.user.player import Player

from whist.server.database.error import PlayerNotCreatorError
from whist.server.services.authentication import get_current_user
from whist.server.services.game_db_service import GameDatabaseService

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/game')


class PlayerNotReadyError(Exception):
    """
    Will check to see if player is ready before unreadying
    """
    pass


class GameNotFoundError(Exception):
    """
    Checks to see if user enters correct game_id
    """
    pass


class StartModel(BaseModel):
    """
    A model to ease data posting to start a game.
    """
    matcher_type: Optional[str] = None

    @property
    def matcher(self) -> Matcher:
        """
        Gets the matcher posted to start the route.
        """
        return RoundRobinMatcher if self.matcher_type == 'robin' else RandomMatcher


@router.post('/action/start/{game_id}', status_code=200)
def start_game(game_id: str, model: StartModel,
               user: Player = Security(get_current_user),
               game_service=Depends(GameDatabaseService)) -> dict:
    """
    Allows the creator of the table to start it.
    :param game_id: unique identifier of the game
    :param model: model containing configuration of the game.
    :param user: Required to identify if the user is the creator.
    :param game_service: Injection of the game database service. Requires to interact with the
    database.
    :return: dictionary containing the status of whether the table has been started or not.
    Raises 403 exception if the user has not the appropriate privileges.
    """
    game = game_service.get(game_id)

    try:
        game.start(user, model.matcher)
        game_service.save(game)
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
    else:
        logger.info(user.username + " has started " + game)
        return {'status': 'started'}


@router.post('/action/ready/{game_id}', status_code=200)
def ready_player(game_id: str, user: Player = Security(get_current_user),
                 game_service=Depends(GameDatabaseService)) -> dict:
    """
    A player can mark theyself to be ready.
    :param game_id: unique identifier of the game
    :param user: Required to identify the user.
    :param game_service: Injection of the game database service. Requires to interact with the
    database.
    :return: dictionary containing the status of whether the action was successful.
    Raises 403 exception if the user has not be joined yet.
    """

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
    logger.info(user.username + " has started " + game)
    return {'status': f'{user.username} is ready'}


@router.post('/action/unready/{game_id}', status_code=200)
def unready_player(game_id: str, user: Player = Security(get_current_user),
                   game_service=Depends(GameDatabaseService)) -> dict:
    """
    A player can mark themself to be unready.
    :param game_id: unique identifier of the game
    :param user: Required to identify the user.
    :param game_service: Injection of the game database service. Requires to interact with the
    database.
    :return: dictionary containing the status of whether the action was successful.
    Raises 403 exception if the user has not be joined yet.
    Raises 404 exception if game_id is not found
    Raises 400 exception if player is not ready
    """

    game = game_service.get(game_id)

    try:
        game.unready_player(user)
        game_service.save(game)
    except PlayerNotJoinedError as join_error:
        message = 'Player not joined yet.'
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
            headers={"WWW-Authenticate": "Basic"},
        ) from join_error
    except GameNotFoundError as game_error:
        message = "Game-id not found"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
            headers={"WWW-Authenticate": "Basic"},
        ) from game_error
    except PlayerNotReadyError as ready_error:
        message = "Player not ready"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
            headers={"WWW-Authenticate": "Basic"},
        ) from ready_error
    return {'status': f'{user.username} is unready'}
