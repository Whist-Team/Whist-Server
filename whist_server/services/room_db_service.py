"""Room database connector"""
from typing import Optional

import bson.errors
from bson import ObjectId
from whist_core.user.player import Player

from whist_server.database import db
from whist_server.database.room import RoomInDb
from whist_server.database.user import UserInDb
from whist_server.services.error import RoomNotFoundError, RoomNotUpdatedError
from whist_server.services.user_db_service import UserDatabaseService


class RoomDatabaseService:
    """
    Handles interactions with the room database.
    """
    _instance = None
    _rooms = None

    def __new__(cls):
        """Creates a new instance of this service singleton."""
        if cls._instance is None:
            cls._instance = super(RoomDatabaseService, cls).__new__(cls)
            cls._rooms = db.room
        return cls._instance

    # pylint: disable=too-many-arguments
    @classmethod
    def create_with_pwd(cls, room_name: str, creator: Player, hashed_password: Optional[str] = None,
                        min_player: Optional[int] = None,
                        max_player: Optional[int] = None) -> RoomInDb:
        """
        Factory method to create a Room in database object.
        :param room_name: name of this session
        :param creator: player object of the host
        :param hashed_password: the hash value of the password required to join
        :param min_player: the minimum amount of player to start a room
        :param max_player: the maximum amount of player that can join this session
        :return: the Room object
        """
        min_player = 4 if min_player is None else int(min_player)
        max_player = 4 if max_player is None else int(max_player)
        room = RoomInDb.create(room_name, creator, min_player, max_player)
        return RoomInDb(**room.model_dump(), hashed_password=hashed_password)

    @classmethod
    def add(cls, room: RoomInDb) -> str:
        """
        Adds a room to the database.
        :param room: to be added
        :return: The id of the successful added room.
        """
        try:
            room: RoomInDb = cls.get_by_name(room.room_name)
            return str(room.id)
        except RoomNotFoundError:
            room_id = cls._rooms.insert_one(room.model_dump(exclude={'id'}))
            return str(room_id.inserted_id)

    @classmethod
    def all(cls) -> list[RoomInDb]:
        """
        Returns all rooms in the database.
        """
        return [RoomInDb(**room) for room in cls._rooms.find()]

    @classmethod
    def get(cls, room_id: str) -> RoomInDb:
        """
        Retrieves a room from the database.
        :param room_id: of the room
        :return: the room database object
        """
        try:
            room = cls._rooms.find_one(ObjectId(room_id))
        except bson.errors.InvalidId as id_error:
            raise RoomNotFoundError(room_id) from id_error
        if room is None:
            raise RoomNotFoundError(room_id)
        return RoomInDb(**room)

    @classmethod
    def get_by_name(cls, room_name: str) -> RoomInDb:
        """
        Similar to 'get(room_id)', but queries by room_name instead of room id.
        :param room_name: of the room
        :return: the room database object
        """
        room = cls._rooms.find_one({'table.name': room_name})
        if room is None:
            raise RoomNotFoundError(game_name=room_name)
        return RoomInDb(**room)

    @classmethod
    def get_by_user_id(cls, user_id: str) -> RoomInDb:
        """
        Retrieves the room a user has joined.
        :param user_id: of the user for which the room should be retrieved
        :return: The room if user has joined one, else RoomNotFoundError
        """
        user_service = UserDatabaseService()
        user: UserInDb = user_service.get(user_id)
        room = cls._rooms.find_one({f'table.users.users.{user.username}': {'$exists': True}})
        if room is None:
            raise RoomNotFoundError()
        return RoomInDb(**room)

    @classmethod
    def save(cls, room: RoomInDb) -> None:
        """
        Saves an updated room object to the database.
        :param room: updated room object
        :return: None. Raises RoomNotFoundError if it could not find a room with that ID. Raises
        a general RoomNotUpdatedError if the room could not be saved.
        """
        query = {'_id': ObjectId(room.id)}
        values = {'$set': room.model_dump(mode='json')}
        result = cls._rooms.update_one(query, values)
        if result.matched_count != 1:
            raise RoomNotFoundError(room.id)
        if result.modified_count != 1:
            raise RoomNotUpdatedError(room.id)
