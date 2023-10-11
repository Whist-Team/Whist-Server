"""A Whist game server using FastAPI"""
import whist_core
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from whist_server.api import api
from whist_server.api.oauth2.github import router as github
from whist_server.api.ranking.leaderboard import router as leaderboard
from whist_server.api.room import room_router
from whist_server.api.user import auth
from whist_server.api.user.create import router as user_creation
from whist_server.api.user.info import router as user_info
from whist_server.services.game_info_service import GameInfoService
from whist_server.web_socket.entry import router as ws_router

# remember to also update the version in pyproject.toml!
__version__ = '0.7.0'

app = FastAPI()
app.include_router(api.router)
app.include_router(github)
app.include_router(room_router)
app.include_router(leaderboard)
app.include_router(user_creation)
app.include_router(user_info)
app.include_router(auth.router)
app.include_router(ws_router)
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])
game_info_db_service = GameInfoService()

game_info = {
    'game': 'whist',
    'whist-core': whist_core.__version__,
    'whist-server': __version__
}
game_info_db_service.add(game_info)
