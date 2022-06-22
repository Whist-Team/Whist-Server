"""Game database connector"""
from typing import Optional

from bson import ObjectId
from whist.core.user.player import Player

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

    # pylint: disable=too-many-arguments
    @classmethod
    def create_with_pwd(cls, game_name: str, creator: Player, hashed_password: Optional[str] = None,
                        min_player: Optional[int] = None,
                        max_player: Optional[int] = None) -> 'GameInDb':
        """
        Factory method to create a Game in database object.
        :param game_name: name of this session
        :param creator: player object of the host
        :param hashed_password: the hash value of the password required to join
        :param min_player: the minimum amount of player to start a game
        :param max_player: the maximum amount of player that can join this session
        :return: the Game object
        """
        min_player = 4 if min_player is None else int(min_player)
        max_player = 4 if max_player is None else int(max_player)
        game = GameInDb.create(game_name, creator, min_player, max_player)
        return GameInDb(**game.dict(), hashed_password=hashed_password)

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
    def all(cls) -> [GameInDb]:
        """
        Returns all games in the database.
        """
        return [GameInDb(**game) for game in cls._games.find()]

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
