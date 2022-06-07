"""Handles all internal request related to ranking and ratings of users."""
from whist.core.user.player import Player

from whist.server.database import db

ASCENDING = 1
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
    def all(cls, order: int) -> list[Player]:
        """
        Returns a list of all users in order of their rating.
        :param order: Integer either 1 for ascending or -1 for descending order.
        """
        ranked_users = cls._user.find().sort({'rating': order})
        return ranked_users
