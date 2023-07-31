"""Room models"""
from enum import Enum, auto
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from whist_core.game.hand import Hand
from whist_core.game.player_at_table import PlayerAtTable
from whist_core.game.rubber import Rubber
from whist_core.game.trick import Trick
from whist_core.session.matcher import Matcher, RandomMatcher
from whist_core.session.table import Table
from whist_core.user.player import Player

from whist_server.database.error import PlayerNotCreatorError, PlayerNotJoinedError
from whist_server.database.id_wrapper import PyObjectId
from whist_server.database.warning import PlayerAlreadyJoinedWarning
from whist_server.services.password import PasswordService


class Room(BaseModel):
    """
    Room DAO
    id: unique identifier for a room.
    creator: user id as string of the player how created that session.
    players: list of user ids of player that joined the roo,.
    side_channel: Communication for all clients
    """
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    creator: Player
    table: Table = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # pylint: disable=too-many-arguments
    @classmethod
    def create(cls, room_name: str, creator: Player,
               min_player: int, max_player: int, matcher: Optional[Matcher] = None) -> 'Room':
        """
        Factory method to create a Room object.
        :param room_name: name of the session
        :param creator: player object of the host
        :param min_player: the minimum amount of player to start a room
        :param max_player: the maximum amount of player that can join this session
        :param matcher: Algorithm to reassign players to teams.
        :return: the room object
        """
        matcher = matcher if isinstance(matcher, Matcher) else RandomMatcher(number_teams=2)
        table = Table(name=room_name, min_player=min_player, max_player=max_player, matcher=matcher)
        if matcher is not None:
            table.matcher = matcher
        table.join(creator)
        return Room(creator=creator, table=table)

    @property
    def room_name(self) -> str:
        """
        :return: name of the room.
        """
        return self.table.name

    @property
    def players(self) -> list[Player]:
        """
        :return: list of user ids that joined the room.
        """
        return self.table.users.players

    @property
    def current_rubber(self) -> Rubber:
        """
        Retrieves the current rubber of the room.
        """
        return self.table.current_rubber

    def current_trick(self) -> Trick:
        """
        Returns the current trick if it exists regardless of being done.
        """
        return self._current_hand().current_trick

    def next_hand(self) -> Hand:
        """
        Creates the next hand.
        """
        return self._current_game().next_hand()

    def next_trick(self) -> Trick:
        """
        Creates the next trick.
        """
        return self._current_hand().next_trick(self._current_game().play_order)

    def join(self, user: Player) -> bool:
        """
        Adds the user to this room.
        :param user: user that wants to join.
        :return: True if successful else an error or warning is raised.
        :raise: PlayerAlreadyJoinedWarning when a player tries to join again.
        """
        if self.has_joined(user):
            raise PlayerAlreadyJoinedWarning(
                f'User with name "{user.username}" has already joined.')
        self.table.join(user)
        return True

    def leave(self, user: Player) -> bool:
        """
        Removes the user to this room.
        :param user: user that wants to leave.
        :return: True if successful else an error or warning is raised.
        """
        if not self.has_joined(user):
            raise PlayerNotJoinedError(
                f'User with name "{user.username}" has joined yet.')
        self.table.leave(user)
        return True

    def has_joined(self, player: Player) -> bool:
        """
        Checks if player has joined the table.
        :param player: to be checked
        :return: True if joined else false.
        """
        return player in self.players

    def ready_player(self, player: Player) -> None:
        """
        Marks a player ready to play.
        :param player: The player who wants to mark themself ready.
        :return: None. Raises PlayerNotJoined if a player tries to get ready without joining a
        table.
        """
        self.table.player_ready(player)

    def start(self, player: Player) -> bool:
        """
        Starts the current table, if the player is the creator.
        :param player: who tries to start the table
        :return: True if successful else False.
        """
        if player != self.creator:
            raise PlayerNotCreatorError()
        if not self.table.started:
            self.table.start()
        started = self.table.started
        self.table.current_rubber.next_game()
        return started

    def get_player(self, player) -> PlayerAtTable:
        """
        Gets the player at table for player instance.
        :param player: for which the player at table is requested.
        :return: PlayerAtTable
        """
        return self.current_rubber.games[-1].get_player(player)

    def _current_hand(self):
        return self._current_game().current_hand

    def _current_game(self):
        return self.current_rubber.current_game()


class RoomInDb(Room):
    """
    room DO
    """
    hashed_password: Optional[bytes] = None

    @property
    def has_password(self) -> bool:
        """
        Returns if the room is password protected.
        """
        return bool(self.hashed_password)

    def verify_password(self, password: Optional[str]):
        """
        Verifies the password for a specific user.
        :param password: plain text of the password
        :return: True if verified or there was not password set in the first place. All other
        cases returns False.
        """
        if self.hashed_password is None and password is None:
            return True
        return PasswordService.verify(password, self.hashed_password)

    def get_info(self) -> 'RoomInfo':
        """
        Returns the meta wrapper of the room.
        :return: RoomInfo
        """
        return RoomInfo.from_room(self)


class RoomPhase(Enum):
    """
    Describes the phase a room can be.
    """
    LOBBY = auto()
    PLAYING = auto()


class RoomInfo(BaseModel):
    """
    Meta info wrapper for rooms.
    """
    name: str
    password: bool
    phase: RoomPhase
    rubber_number: int
    game_number: int
    hand_number: int
    trick_number: int
    min_player: int
    max_player: int
    players: list[Player]

    @staticmethod
    def from_room(room: RoomInDb) -> 'RoomInfo':
        """
        Creates a room info object from a room.
        :param room: Meta data extracted from
        :return: RoomInfo
        """
        phase: RoomPhase = RoomPhase.PLAYING if room.table.started else RoomPhase.LOBBY
        password_protected = room.has_password
        rubber_number = len(room.table.current_rubber.games) if room.table.started else 0
        trick_number = len(room.table.current_rubber.current_game().current_hand.tricks) if \
            room.table.started else 0
        return RoomInfo(name=room.room_name,
                        password=password_protected,
                        phase=phase,
                        rubber_number=len(room.table.rubbers),
                        game_number=rubber_number,
                        hand_number=0,
                        trick_number=trick_number,
                        min_player=room.table.min_player,
                        max_player=room.table.max_player,
                        players=room.table.users.players)
