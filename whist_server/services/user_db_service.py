"""User database connector."""
from bson import ObjectId

from whist_server.database import db
from whist_server.database.user import UserInDb
from whist_server.services.error import UserNotFoundError, UserExistsError


class UserDatabaseService:
    """
    Handles interaction with user database.
    """
    _instance = None
    _users = None

    def __new__(cls):
        """Creates a new instance of this service singleton."""
        if cls._instance is None:
            cls._instance = super(UserDatabaseService, cls).__new__(cls)
            cls._users = db.user
        return cls._instance

    @classmethod
    def add(cls, user: UserInDb) -> str:
        """
        Adds a user to the database.
        :param user: to be added
        :return: The id of the successful added user.
        """
        try:
            _ = cls.get_by_username(user.username)
        except UserNotFoundError:
            user_id = cls._users.insert_one(user.dict(exclude={'id'}))
            return str(user_id.inserted_id)

        raise UserExistsError(f'User with username: "{user.username}" already exists.')

    @classmethod
    def get(cls, user_id: str) -> UserInDb:
        """
        Gets the user querying the user ID.
        :param user_id: of the user
        :return: the user database object
        """
        user = cls._users.find_one({'_id': ObjectId(user_id)})
        if user is None:
            raise UserNotFoundError()
        return UserInDb(**user)

    @classmethod
    def get_by_username(cls, username: str) -> UserInDb:
        """
        Gets the user querying the username.
        :param username: of the user
        :return: the user database object
        """
        user = cls._users.find_one({'username': username})
        if user is None:
            raise UserNotFoundError(username=username)
        return UserInDb(**user)

    @classmethod
    def get_from_github(cls, github_id: str) -> UserInDb:
        """
        Similar to 'get(username)', but queries by github username instead of application username.
        :param github_id: GitHub id of the user
        :return: the user database object
        """
        user = cls._users.find_one({'github_id': github_id})
        if user is None:
            raise UserNotFoundError()
        return UserInDb(**user)
