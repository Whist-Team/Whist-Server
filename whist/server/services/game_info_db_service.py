"""Game Info database connector"""


class GameInfoDatabaseService:
    """
    Handles interaction with the game info database.
    """
    _instance = None
    _info: dict = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameInfoDatabaseService, cls).__new__(cls)
            cls._info = {}

        return cls._instance

    @classmethod
    def add(cls, info: dict) -> None:
        """
        Adds game info to the database. It can only contains one at a time.
        :param info: to be added
        :return: None
        """
        cls._info.update(info)

    @classmethod
    def get(cls):
        """
        Retrieves the game info object. There is only one.
        :return: Game info object if it is exists. Else raises GameInfoNotSetError.
        """
        return cls._info
