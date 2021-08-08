"""'/user/create api"""
from typing import Dict

from whist.server.api.user import router
from whist.server.database import db
from whist.server.database.user import UserInDb
from whist.server.services.password import PasswordService


@router.post('/create')
def create_user(request: Dict[str, str]):
    """
    Creates a new user.
    :return: the ID of the user or an error message.
    """
    pwd_service = PasswordService()
    pwd_hash = pwd_service.hash(request['password'])
    user = UserInDb(username=request['username'],
                    hashed_password=pwd_hash)
    user_dict = user.dict()
    user_dict.pop('id')
    user_id = db.user.insert_one(user_dict)
    return {'user_id': str(user_id.inserted_id)}
