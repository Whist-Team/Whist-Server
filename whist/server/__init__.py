"""A Whist game server using FastAPI"""
import pkg_resources
from fastapi import FastAPI

from whist.server.api import api
from whist.server.api.game.action import router as game_action
from whist.server.api.game.create import router as game_creation
from whist.server.api.game.info import router as game_info
from whist.server.api.game.join import router as game_join
from whist.server.api.game.trick import router as game_trick
from whist.server.api.ranking.leaderboard import router as leaderboard
from whist.server.api.user import auth
from whist.server.api.user.create import router as user_creation
from whist.server.database.game_info import GameInfo
from whist.server.services.game_info_db_service import GameInfoDatabaseService
from whist.server.web_socket.entry import router as ws_router

app = FastAPI()
app.include_router(api.router)
app.include_router(game_action)
app.include_router(game_creation)
app.include_router(game_info)
app.include_router(game_join)
app.include_router(game_trick)
app.include_router(leaderboard)
app.include_router(user_creation)
app.include_router(auth.router)
app.include_router(ws_router)
game_info_db_service = GameInfoDatabaseService()

for module in ['whist-core', 'whist-server']:
    version = pkg_resources.get_distribution(module).version
    game_info = GameInfo(game=module, version=version)
    game_info_db_service.add(game_info)
