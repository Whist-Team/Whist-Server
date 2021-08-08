"""A Whist game server using FastAPI"""
import pkg_resources
from fastapi import FastAPI

from whist.server.api import api
from whist.server.api.user import create
from whist.server.database import GameInfo
from whist.server.services.game_info_db_service import GameInfoDatabaseService

app = FastAPI()
app.include_router(api.router)
app.include_router(create.router)

whist_core_version = pkg_resources.get_distribution('whist-core').version
game_info = GameInfo(game='whist', version=whist_core_version)
game_info_db_service = GameInfoDatabaseService()
game_info_db_service.add(game_info)
