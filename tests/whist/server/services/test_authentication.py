from datetime import timedelta

import pytest
from bson import ObjectId

from whist.server.database.user import UserInDb
from whist.server.services.authentication import get_current_user, create_access_token, \
    check_credentials
from whist.server.services.error import UserNotFoundError, CredentialsException
from whist.server.services.password import PasswordService
from whist.server.services.user_db_service import UserDatabaseService


def _create_user():
    hashed_password = PasswordService().hash('abc')
    user = UserInDb(username='test', hashed_password=hashed_password)
    user_db_service = UserDatabaseService()
    user.id = ObjectId(user_db_service.add(user))
    return user


@pytest.mark.asyncio
async def test_get_current_user():
    user = _create_user()
    token = create_access_token(data={'sub': user.username})
    result_user = await get_current_user(token)
    assert user.to_user() == result_user


@pytest.mark.asyncio
async def test_get_current_user_no_user():
    user = _create_user()
    token = create_access_token(data={'sub': user.username})
    result_user = await get_current_user(token)
    assert user.to_user() == result_user


@pytest.mark.asyncio
async def test_get_current_user_with_delta():
    token = create_access_token(data={'sub': 'test'})
    with pytest.raises(UserNotFoundError):
        _ = await get_current_user(token)


@pytest.mark.asyncio
async def test_check_credentials():
    _ = _create_user()
    is_valid = await check_credentials('test', 'abc')
    assert is_valid


@pytest.mark.asyncio
async def test_check_wrong_credentials():
    _ = _create_user()
    is_valid = await check_credentials('test', 'abcd')
    assert not is_valid


@pytest.mark.asyncio
async def test_check_no_user():
    _ = _create_user()

    with pytest.raises(UserNotFoundError):
        _ = await check_credentials('marcel', 'abc')
