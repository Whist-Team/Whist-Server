from typing import Dict

from fastapi import APIRouter, Security
from whist.core.user.player import Player
from whist.server.services.authentication import get_current_user

router = APIRouter(prefix='/game')


@router.post('/action/start/{game_id}', status_code=200)
def start_game(game_id: str, user: Player = Security(get_current_user)):
    return {'status': 'started'}
