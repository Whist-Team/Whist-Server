"""A Whist game server using FastAPI"""

from fastapi import FastAPI

from whist.server.api.game.create import router as game_creation
from whist.server.api.user.create import router as user_creation
from .api import api, user

app = FastAPI()
app.include_router(api.router)
app.include_router(game_creation)
app.include_router(user_creation)
