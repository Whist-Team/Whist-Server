"""User database connector."""

from whist.server.database import db
from whist.server.database.user import UserInDb
from whist.server.services.error import UserNotFoundError, UserExistsError


class UserDatabaseService:
    """
    Handles interaction with user database.
    """
    _instance = None
    _users = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserDatabaseService, cls).__new__(cls)
            cls._users = db.user
        return cls._instance

    @classmethod
    def add(cls, user: UserInDb) -> str:
        """
        Adds an user to the database.
        :param user: to be added
        :return: The id of the successful added user.
        """
        try:
            _ = cls.get(user.username)
        except UserNotFoundError:
            user_id = cls._users.insert_one(user.dict(exclude={'id'}))
            return str(user_id.inserted_id)
        else:
            raise UserExistsError(f'User with username: "{user.username}" already exists.')

    @classmethod
    def get(cls, username: str) -> UserInDb:
        """
        Similar to 'get(user_id)', but queries by username instead of user id.
        :param username: of the user
        :return: the user database object
        """
        user = cls._users.find_one({'username': username})
        if user is None:
            raise UserNotFoundError(username=username)
        return UserInDb(**user)
