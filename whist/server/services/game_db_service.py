"""Game database connector"""
from bson import ObjectId

from whist.server.database import db
from whist.server.database.game import GameInDb
from whist.server.services.error import GameNotFoundError, GameNotUpdatedError


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
        try:
            game: GameInDb = cls.get_by_name(game.game_name)
            return str(game.id)
        except GameNotFoundError:
            game_id = cls._games.insert_one(game.dict(exclude={'id'}))
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

    @classmethod
    def get_by_name(cls, game_name: str) -> GameInDb:
        """
        Similar to 'get(game_id)', but queries by game_name instead of game id.
        :param game_name: of the game
        :return: the game database object
        """
        game = cls._games.find_one({'table.name': game_name})
        if game is None:
            raise GameNotFoundError(game_name=game_name)
        return GameInDb(**game)

    @classmethod
    def save(cls, game: GameInDb) -> None:
        """
        Saves an updated game object to the database.
        :param game: updated game object
        :return: None. Raises GameNotFoundError if it could not find a game with that ID. Raises
        a general GameNotUpdatedError if the game could not be saved.
        """
        query = {'_id': ObjectId(game.id)}
        values = {'$set': game.dict()}
        result = cls._games.update_one(query, values)
        if result.matched_count != 1:
            raise GameNotFoundError(game.id)
        if result.modified_count != 1:
            raise GameNotUpdatedError(game.id)
