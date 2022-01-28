from typing import Union

from fastapi import APIRouter, Security, HTTPException, status
from whist.core.cards.card import Card
from whist.core.cards.card_container import OrderedCardContainer
from whist.core.game.errors import NotPlayersTurnError
from whist.core.game.player_at_table import PlayerAtTable
from whist.core.game.warnings import TrickNotDoneWarning
from whist.core.user.player import Player

from whist.server.services.authentication import get_current_user
from whist.server.services.game_db_service import GameDatabaseService

router = APIRouter(prefix='/game/trick')


@router.post('/play_card/{game_id}', status_code=200, response_model=OrderedCardContainer)
def play_card(game_id: str, card: Card,
              user: Player = Security(get_current_user)) -> OrderedCardContainer:
    game_service = GameDatabaseService()
    room = game_service.get(game_id)

    try:
        trick = room.current_trick
        player = room.get_player(user)
        trick.play_card(player=player, card=card)
        game_service.save(room)
    except NotPlayersTurnError as turn_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            headers={"WWW-Authenticate": "Basic"}) from turn_error
    return trick.stack


@router.get('/winner/{game_id}', status_code=200,
            response_model=Union[PlayerAtTable, dict[str, str]])
def winner(game_id: str, user: Player = Security(get_current_user)) -> Union[PlayerAtTable,
                                                                             dict[str, str]]:
    game_service = GameDatabaseService()
    room = game_service.get(game_id)
    if not user in room.players:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            headers={'WWW-Authenticate': 'Basic'},
                            detail='You have not joined the table.')

    trick = room.current_trick
    try:
        winner = trick.winner
    except TrickNotDoneWarning:
        return {'status': 'The trick is not yet done, so there is no winner.'}
    return winner
