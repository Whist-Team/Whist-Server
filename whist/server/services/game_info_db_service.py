"""Game Info database connector"""
from whist.server.database.game_info import GameInfo


class GameInfoDatabaseService:
    """
    Handles interaction with the game info database.
    """
    _instance = None
    _info: list[GameInfo] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameInfoDatabaseService, cls).__new__(cls)
            cls._info = []

        return cls._instance

    @classmethod
    def add(cls, info: GameInfo) -> None:
        """
        Adds game info to the database. It can only contains one at a time.
        :param info: to be added
        :return: None
        """
        cls._info.append(info)

    @classmethod
    def get(cls):
        """
        Retrieves the game info object. There is only one.
        :return: Game info object if it is exists. Else raises GameInfoNotSetError.
        """
        return cls._info
