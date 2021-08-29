"""'/user/create api"""
from typing import Dict

from fastapi import APIRouter

from whist.server.database.user import UserInDb
from whist.server.services.password import PasswordService
from whist.server.services.user_db_service import UserDatabaseService

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
    user_db_service = UserDatabaseService()
    user_id = user_db_service.add(user)
    return {'user_id': user_id}
