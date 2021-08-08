"""Route of /game/creation"""
from typing import Dict

from fastapi import APIRouter, HTTPException

from whist.server.database import db
from whist.server.database.game import GameInDb
from whist.server.services.password import PasswordService

router = APIRouter(prefix='/game')


@router.post('/create', status_code=201)
def create_game(request: Dict[str, str]):
    """
    Creates a new game of whist.
    :param request: Must contain a 'game_name'. 'password' is optional.
    :return: the ID of the game instance.
    """
    pwd_service = PasswordService()
    pwd_hash = _get_password(pwd_service, request)
    game_name = _get_game_name(request)

    game = GameInDb(game_name=game_name,
                    password=pwd_hash)
    game_dict: dict = game.dict()
    game_dict.pop('id')
    game_id = db.game.insert_one(game_dict)
    return {'game_id': str(game_id.inserted_id)}


def _get_game_name(request):
    try:
        game_name = request['game_name']
    except KeyError as key_error:
        raise HTTPException(status_code=400, detail='"game_name" is required.') from key_error
    return game_name


def _get_password(pwd_service, request):
    try:
        password = request['password']
        pwd_hash = pwd_service.hash(password)
    except KeyError:
        pwd_hash = None
    return pwd_hash
