"""'/user/create api"""
from typing import Dict

from fastapi import APIRouter, HTTPException

from whist.server.database.user import UserInDb
from whist.server.services.password import PasswordService
from whist.server.services.user_db_service import UserDatabaseService

router = APIRouter(prefix='/user')


@router.post('/create')
def create_user(request: Dict[str, str]):
    """
    Creates a new user.
    :param request: Must contain a 'username' and a 'password' field. If one is missing it raises
    HTTP 400 error.
    :return: the ID of the user or an error message.
    """
    pwd_service = PasswordService()
    try:
        pwd_hash = pwd_service.hash(request['password'])
    except KeyError as key_error:
        raise HTTPException(status_code=400,
                            detail='A password is required to create a user.') from key_error
    try:
        username = request['username']
    except KeyError as key_error:
        raise HTTPException(status_code=400,
                            detail='A username is required to create a user.') from key_error
    user = UserInDb(username=username,
                    hashed_password=pwd_hash)
    user_db_service = UserDatabaseService()
    user_id = user_db_service.add(user)
    return {'user_id': user_id}
