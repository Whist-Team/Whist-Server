"""A Whist game server using FastAPI"""

from fastapi import FastAPI

from whist.server import api

app = FastAPI()
app.include_router(api.router)
