"""A Whist game server using FastAPI"""

from fastapi import FastAPI

from server import api

app = FastAPI()
app.include_router(api.router)
