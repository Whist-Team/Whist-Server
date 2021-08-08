"""A Whist game server using FastAPI"""

from fastapi import FastAPI

from whist.server.api import api, game, user

app = FastAPI()
app.include_router(api.router)
app.include_router(game.router)
app.include_router(user.router)
