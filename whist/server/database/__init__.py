from whist.server.database.connection import get_database
from whist.server.database.game_info import GameInfo

db = get_database()

game_info = GameInfo(game='whist', version='0.1.0rc2')
db.info.insert_one(game_info.dict(by_alias=True))
