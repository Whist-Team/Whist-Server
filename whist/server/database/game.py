"""Game models"""
from typing import Optional

from pydantic import BaseModel, Field
from whist.core.session.table import Table
from whist.core.user.player import Player

from whist.server.database.id_wrapper import PyObjectId
from whist.server.services.password import PasswordService


class Game(BaseModel):
    """
    Game DAO
    id: unique identifier for a game.
    game_name: user friendly identifier
    creator: user id as string of the player how created that session.
    players: list of user ids of player that joined the game.
    """
    id: Optional[PyObjectId] = Field(alias='_id')
    creator: Player
    table: Table = None

    @classmethod
    def create(cls, game_name: str, creator: Player,
               min_player: int = 4, max_player: int = 4) -> 'Game':
        table = Table(name=game_name, min_player=min_player, max_player=max_player)
        table.join(creator)
        return Game(creator=creator, table=table)

    @property
    def game_name(self) -> str:
        """
        :return: name of the game.
        """
        return self.table.name


class GameInDb(Game):
    """
    Game DO
    """
    hashed_password: Optional[str]

    @classmethod
    def create_with_pwd(cls, game_name: str, creator: Player, hashed_password: str,
                        min_player: int = 4, max_player: int = 4) -> 'GameInDb':
        game = super().create(game_name, creator, min_player, max_player)
        return GameInDb(**game.dict(), hashed_password=hashed_password)

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
