from typing import Dict

from whist.server.api.game import router
from whist.server.database import db
from whist.server.database.game import GameInDb


@router.post('/create', status_code=201)
def create_game(request: Dict[str, str]):
    """
    Creates a new game of whist.
    :param request: Must contain a 'game_name'. 'password' is optional.
    :return: the ID of the game instance.
    """
    pwd_hash = request['password'] if request['password'] else None
    game = GameInDb(game_name=request['game_name'],
                    password=pwd_hash)
    game_dict: dict = game.dict()
    game_dict.pop('id')
    game_id = db.game.insert_one(game_dict)
    return {'game_id': str(game_id.inserted_id)}
