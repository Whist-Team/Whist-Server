"""A Whist game server using FastAPI"""

from fastapi import FastAPI

from whist.server.api import api
from whist.server.api.user import create

app = FastAPI()
app.include_router(api.router)
app.include_router(create.router)
