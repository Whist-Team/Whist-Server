"""A Whist game server using FastAPI"""
import pkg_resources
from fastapi import FastAPI

from whist.server.api import api
from whist.server.api.game.action import router as game_action
from whist.server.api.game.create import router as game_creation
from whist.server.api.game.join import router as game_join
from whist.server.api.game.trick import router as game_trick
from whist.server.api.user import auth
from whist.server.api.user.create import router as user_creation
from whist.server.database.game_info import GameInfo
from whist.server.services.game_info_db_service import GameInfoDatabaseService

app = FastAPI()
app.include_router(api.router)
app.include_router(game_action)
app.include_router(game_creation)
app.include_router(game_join)
app.include_router(game_trick)
app.include_router(user_creation)
app.include_router(auth.router)

whist_core_version = pkg_resources.get_distribution('whist-core').version
game_info = GameInfo(game='whist', version=whist_core_version)
game_info_db_service = GameInfoDatabaseService()
game_info_db_service.add(game_info)
