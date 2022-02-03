"""Interaction with the current trick of a room."""

from fastapi import APIRouter, Security
from whist.core.cards.card_container import UnorderedCardContainer
from whist.core.user.player import Player

from whist.server.services.authentication import get_current_user
from whist.server.services.game_db_service import GameDatabaseService

router = APIRouter(prefix='/game/trick')


@router.get('/hand/{game_id}', status_code=200, response_model=UnorderedCardContainer)
def hand(game_id: str, user: Player = Security(get_current_user)) -> UnorderedCardContainer:
    """
    Returns the current hand of player.
    :param game_id: unique identifier for which the player's hand is requested
    :param user: for which the hand is requested
    :return: UnorderedCardContainer containing all cards of the player
    """
    game_service = GameDatabaseService()
    room = game_service.get(game_id)

    player = room.get_player(user)
    return player.hand
