"""Game Info database connector"""
from whist.server.database import db, GameInfo


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
        if cls._info.find().count() > 0:
            cls._info.delete_many({})
        cls._info.insert_one(info.dict())

    @classmethod
    def get(cls):
        info: dict = cls._info.find_one()
        info.pop('_id')
        return GameInfo(**info)
