from pymongo import MongoClient

from whist.server.const import DATABASE_NAME, TEST_DATABASE
from whist.server.database.game_info import GameInfo

client = MongoClient()
if DATABASE_NAME == TEST_DATABASE:
    client.drop_database(DATABASE_NAME)
db = client[DATABASE_NAME]

game_info = GameInfo(game='whist', version='0.1.0rc2')
db.info.insert_one(game_info.dict(by_alias=True))
