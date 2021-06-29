"""'/user/create routes"""
from typing import Dict

from fastapi import APIRouter

from whist.server.db import db
from whist.server.models.user import User

router = APIRouter(prefix='/user/create')


@router.post('/')
def create_user(request: Dict[str, str]):
    """
    Creates a new user.
    :return: the ID of the user or an error message.
    """
    user = User(username=request['username'])
    db.insert_one(user)
    return {'user_id': '1'}
