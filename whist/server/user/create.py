"""'/user/create routes"""
from typing import Dict

from fastapi import APIRouter

from whist.server.database import db
from whist.server.database.user import UserInDb
from whist.server.services.password import PasswordService

router = APIRouter(prefix='/user/create')


@router.post('/')
def create_user(request: Dict[str, str]):
    """
    Creates a new user.
    :return: the ID of the user or an error message.
    """
    pwd_service = PasswordService()
    pwd_hash = pwd_service.hash(request['password'])
    user = UserInDb(username=request['username'],
                    hashed_password=pwd_hash)
    db.user.insert_one(user.dict(by_alias=True))
    return {'user_id': '1'}
