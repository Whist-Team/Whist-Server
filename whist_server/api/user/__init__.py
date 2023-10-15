"""User related API"""
from fastapi import APIRouter

from whist_server.api.user.auth import auth_router
from whist_server.api.user.create import create_router
from whist_server.api.user.info import info_router

user_router = APIRouter(prefix='/user')
user_router.include_router(auth_router)
user_router.include_router(create_router)
user_router.include_router(info_router)
