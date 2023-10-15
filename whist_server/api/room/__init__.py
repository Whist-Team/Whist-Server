"""Room related API"""
from fastapi import APIRouter

from whist_server.api.room.action import action_router
from whist_server.api.room.create import create_router
from whist_server.api.room.game import game_router
from whist_server.api.room.info import info_router
from whist_server.api.room.join import join_router
from whist_server.api.room.trick import trick_router

room_router = APIRouter(prefix='/room')
room_router.include_router(action_router)
room_router.include_router(create_router)
room_router.include_router(game_router)
room_router.include_router(info_router)
room_router.include_router(join_router)
room_router.include_router(trick_router)
