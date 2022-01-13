from fastapi import APIRouter, Security
from whist.core.cards.card import Card
from whist.core.cards.stack import Stack
from whist.core.user.player import Player

from whist.server.services.authentication import get_current_user
from whist.server.services.game_db_service import GameDatabaseService

router = APIRouter(prefix='/game/trick')


@router.post('/play_card/{game_id}', status_code=200, response_model=Stack)
def play_card(game_id: str, card: Card, user: Player = Security(get_current_user)) -> Stack:
    game_service = GameDatabaseService()
    room = game_service.get(game_id)

    room.play_card(player=user, card=card)
    return room.current_stack
