"""A Whist game server using FastAPI"""

from fastapi import FastAPI

from whist.server import api
from whist.server.user import create

app = FastAPI()
app.include_router(api.router)
app.include_router(create.router)
