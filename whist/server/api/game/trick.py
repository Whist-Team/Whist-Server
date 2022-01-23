from fastapi import APIRouter, Security, HTTPException, status
from whist.core.cards.card import Card
from whist.core.cards.card_container import OrderedCardContainer
from whist.core.game.errors import NotPlayersTurnError
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
        room.play_card(player=user, card=card)
        game_service.save(room)
    except NotPlayersTurnError as turn_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            headers={"WWW-Authenticate": "Basic"}) from turn_error
    return room.current_stack
