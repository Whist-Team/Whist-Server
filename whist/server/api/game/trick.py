"""Interaction with the current trick of a room."""
from typing import Union

from fastapi import APIRouter, Security, Depends
from fastapi import HTTPException, status
from whist.core.cards.card import Card
from whist.core.cards.card_container import OrderedCardContainer
from whist.core.cards.card_container import UnorderedCardContainer
from whist.core.game.errors import NotPlayersTurnError
from whist.core.game.player_at_table import PlayerAtTable
from whist.core.game.warnings import TrickNotDoneWarning
from whist.core.user.player import Player

from whist.server.services.authentication import get_current_user
from whist.server.services.game_db_service import GameDatabaseService

import logging
import sys

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(levelname)s:%(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

router = APIRouter(prefix='/game/trick')


@router.get('/hand/{game_id}', status_code=200, response_model=UnorderedCardContainer)
def hand(game_id: str, user: Player = Security(get_current_user),
         game_service=Depends(GameDatabaseService)) -> UnorderedCardContainer:
    """
    Returns the current hand of player.
    :param game_id: unique identifier for which the player's hand is requested
    :param user: for which the hand is requested
    :param game_service: Injection of the game database service. Requires to interact with the
    database.
    :return: UnorderedCardContainer containing all cards of the player
    """
    room = game_service.get(game_id)

    player = room.get_player(user)
    return player.hand


@router.post('/play_card/{game_id}', status_code=200, response_model=OrderedCardContainer)
def play_card(game_id: str, card: Card,
              user: Player = Security(get_current_user),
              game_service=Depends(GameDatabaseService)) -> OrderedCardContainer:
    """
    Request to play a card for a given game.
    :param game_id: at which table the card is requested to be played
    :param card: which is requested to be played
    :param user: who to played a card
    :param game_service: Injection of the game database service. Requires to interact with the
    database.
    :return: the stack after card being played if successful. If not the players turn raises error.
    """
    room = game_service.get(game_id)

    try:
        trick = room.current_trick(auto_next=True)
        player = room.get_player(user)
        trick.play_card(player=player, card=card)
        game_service.save(room)
    except NotPlayersTurnError as turn_error:
        raise HTTPException(detail=f'It is not {player.player.username} turn',
                            status_code=status.HTTP_400_BAD_REQUEST,
                            headers={"WWW-Authenticate": "Basic"}) from turn_error
    return trick.stack


@router.get('/winner/{game_id}', status_code=200,
            response_model=Union[PlayerAtTable, dict[str, str]])
def get_winner(game_id: str, user: Player = Depends(get_current_user),
               game_service=Depends(GameDatabaseService)) -> Union[PlayerAtTable, dict[str, str]]:
    """
    Requests the winner of the current stack.
    :param game_id: for which the stack is requested
    :param user: who requested the winner
    :param game_service: Injection of the game database service. Requires to interact with the
    database.
    :return: The PlayerAtTable object of the winner. Raises Exception if the user has not joined
    the game yet. Replies with a warning if the trick has not be done.
    """
    room = game_service.get(game_id)
    if user not in room.players:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            headers={'WWW-Authenticate': 'Basic'},
                            detail='You have not joined the table.')

    trick = room.current_trick()
    try:
        winner = trick.winner
    except TrickNotDoneWarning:
        return {'status': 'The trick is not yet done, so there is no winner.'}
    #return winner
    return logger.info(user.username + " has won")
