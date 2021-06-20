"""'/user/create routes"""

from fastapi import APIRouter
from whist.core.user.user import User

router = APIRouter(prefix='/user/create')


@router.post('/')
def create_user(username: str):
    """
    Creates a new user.
    :return: the ID of the user or an error message.
    """
    user = User(username)
    return user.user_id
