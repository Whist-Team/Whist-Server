"""Handles all internal request related to ranking and ratings of users."""
from whist.core.user.player import Player

from whist.server.database import db

DESCENDING = -1


class RankingService:
    """
    Service to retrieve information of users' ranking based of their rating.
    """
    _instance = None
    _user = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RankingService, cls).__new__(cls)
            cls._users = db.user
        return cls._instance

    @classmethod
    def all(cls) -> list[Player]:
        """
        Returns a list of all users in descending order of their rating.
        """
        ranked_users = cls._user.find().sort({'rating': DESCENDING})
        return ranked_users
