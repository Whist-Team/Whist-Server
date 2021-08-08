"""User database connector."""
from bson import ObjectId

from whist.server.database import db
from whist.server.database.user import UserInDb


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
        user_dict: dict = user.dict()
        user_dict.pop('id')
        user_id = cls._users.insert_one(user_dict)
        return str(user_id.inserted_id)

    @classmethod
    def get(cls, user_id: str) -> UserInDb:
        """
        Retrieves an user from the database.
        :param user_id: of the user
        :return: the user database object
        """
        user = cls._users.find_one(ObjectId(user_id))
        return UserInDb(**user)
