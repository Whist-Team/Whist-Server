"""Game Info provider"""


class GameInfoService:
    """
    Provides information on supported games.
    """
    _instance = None
    _info: dict = None

    def __new__(cls):
        """Creates a new instance of this service singleton."""
        if cls._instance is None:
            cls._instance = super(GameInfoService, cls).__new__(cls)
            cls._info = {}

        return cls._instance

    @classmethod
    def add(cls, info: dict) -> None:
        """
        Adds game info to the list of supported games.
        :param info: to be added
        :return: None
        """
        cls._info.update(info)

    @classmethod
    def get(cls):
        """
        Retrieves the game info object.
        :return: Game info object if it is exists. Else None.
        """
        return cls._info
