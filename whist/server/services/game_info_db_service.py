"""Game Info database connector"""
from whist.server.database import db
from whist.server.database.game_info import GameInfo
from whist.server.services.error import GameInfoNotSetError


class GameInfoDatabaseService:
    """
    Handles interaction with the game info database.
    """
    _instance = None
    _info = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameInfoDatabaseService, cls).__new__(cls)
            cls._info = db.info

        return cls._instance

    @classmethod
    def add(cls, info: GameInfo) -> None:
        """
        Adds game info to the database. It can only contains one at a time.
        :param info: to be added
        :return: None
        """
        if cls._info.estimated_document_count() > 0:
            cls._info.delete_many({})
        cls._info.insert_one(info.dict(exclude={'_id', 'id'}))

    @classmethod
    def get(cls):
        """
        Retrieves the game info object. There is only one.
        :return: Game info object if it is exists. Else raises GameInfoNotSetError.
        """
        info: dict = cls._info.find_one(projection={'_id': False})
        if info is None:
            raise GameInfoNotSetError()
        return GameInfo(**info).copy(exclude={'id'})
