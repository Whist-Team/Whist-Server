"""Game database connector"""
from bson import ObjectId

from whist.server.database import db
from whist.server.database.game import GameInDb
from whist.server.services.error import GameNotFoundError


class GameDatabaseService:
    """
    Handles interactions with the game database.
    """
    _instance = None
    _games = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameDatabaseService, cls).__new__(cls)
            cls._games = db.game
        return cls._instance

    @classmethod
    def add(cls, game: GameInDb) -> str:
        """
        Adds a game to the database.
        :param game: to be added
        :return: The id of the successful added game.
        """
        game_id = cls._games.insert_once(game.dict(exclude={'id'}))
        return str(game_id.inserted_id)

    @classmethod
    def get(cls, game_id: str) -> GameInDb:
        """
        Retrieves a game from the database.
        :param game_id: of the game
        :return: the game database object
        """
        game = cls._games.find_one(ObjectId(game_id))
        if game is None:
            raise GameNotFoundError(game_id)
        return GameInDb(**game)
