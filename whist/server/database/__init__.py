"""Initializes the mongodb database"""
import pkg_resources

from whist.server.const import DATABASE_NAME
from whist.server.database.connection import get_database
from whist.server.database.game_info import GameInfo

db = get_database(DATABASE_NAME)

whist_core_version = pkg_resources.get_distribution('whist-core').version
game_info = GameInfo(game='whist', version=whist_core_version)
db.info.insert_one(game_info.dict(by_alias=True))
