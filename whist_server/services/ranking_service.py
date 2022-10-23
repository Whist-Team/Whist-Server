"""Handles all internal request related to ranking and ratings of users."""
from whist_core.user.player import Player

from whist_server.database import db


class RankingService:
    """
    Service to retrieve information of users' ranking based of their rating.
    """
    _instance = None
    _users = None

    _ASCENDING = 1
    _DESCENDING = -1

    def __new__(cls):
        """Creates a new instance of this service singleton."""
        if cls._instance is None:
            cls._instance = super(RankingService, cls).__new__(cls)
            cls._users = db.user
        return cls._instance

    @classmethod
    def select(cls, order: str, amount: int, start: int) -> list[Player]:
        """
        Returns a list of user limited by starting index and amount in order of their rating.
        :param order: Integer either 1 for ascending or -1 for descending order.
        :param amount: The number of players the list shall contain at max.
        :param start: Skip this number of players from the top.
        """
        user_cursor = cls._get_all_players(order)
        user_cursor.skip(start)
        if amount > 0:
            user_cursor.limit(amount)
        return [Player(**user) for user in user_cursor]

    @classmethod
    def _get_all_players(cls, order):
        """
        Returns a cursor object of all players sorted by their rating.
        :param order:  Integer either 1 for ascending or -1 for descending order.
        """
        mongodb_order = cls._convert_order_to_mongodb(order)
        user_cursor = cls._users.find()
        user_cursor.sort('rating', mongodb_order)
        return user_cursor

    @classmethod
    def _convert_order_to_mongodb(cls, order: str) -> int:
        """
        Converts the string ascending and descending to the required integers 1 and -1
        :param order: string 'ascending' or 'descending'
        :return: 1 or -1
        """
        if order == 'ascending':
            return cls._ASCENDING
        if order == 'descending':
            return cls._DESCENDING

        raise ValueError(f'"order" must either be "ascending" or "descending", but was "{order}"')
