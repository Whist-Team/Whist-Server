import pytest
from bson import ObjectId

from whist.server.database.user import UserInDb
from whist.server.services.authentication import get_current_user, create_access_token
from whist.server.services.user_db_service import UserDatabaseService


@pytest.mark.asyncio
async def test_get_current_user():
    user = UserInDb(username='test', hashed_password='abc')
    user_db_service = UserDatabaseService()
    user.id = ObjectId(user_db_service.add(user))
    token = create_access_token(data={'sub': user.username})
    result_user = await get_current_user(token)
    print(user)
    assert user == result_user
