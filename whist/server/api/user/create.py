"""'/user/create api"""

from fastapi import APIRouter
from pydantic import BaseModel

from whist.server.database.user import UserInDb
from whist.server.services.password import PasswordService
from whist.server.services.user_db_service import UserDatabaseService

router = APIRouter(prefix='/user')


class CreateUserArgs(BaseModel):
    """
    JSON body for creating user
    """
    username: str
    password: str


@router.post('/create')
def create_user(request: CreateUserArgs):
    """
    Creates a new user.
    :param request: Must contain a 'username' and a 'password' field. If one is missing it raises
    HTTP 400 error.
    :return: the ID of the user or an error message.
    """
    pwd_service = PasswordService()
    user = UserInDb(username=request.username, hashed_password=pwd_service.hash(request.password))
    user_db_service = UserDatabaseService()
    user_id = user_db_service.add(user)
    return {'user_id': user_id}
