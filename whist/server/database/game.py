"""Game models"""
from typing import Optional, Any

from pydantic import BaseModel, Field
from whist.core.session.session import Session

from whist.server.database.id_wrapper import PyObjectId
from whist.server.database.warning import PlayerAlreadyJoinedWarning
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
    game_name: str
    creator: str
    session: Session = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.session = Session(creator)

    @property
    def players(self) -> list[str]:
        """
        :return: list of user ids that joined the game.
        """
        return self.user_list

    def join(self, user_id: str) -> bool:
        """
        Adds the user to this game.
        :param user_id: unique identifier of the user
        :return: True if successful else an error or warning is raised.
        :raise: PlayerAlreadyJoinedWarning when a player tries to join again.
        """
        if user_id in self.user_list:
            raise PlayerAlreadyJoinedWarning(f'User with id "{user_id}" has already joined.')
        self.user_list.append(user_id)
        return True


class GameInDb(Game):
    """
    Game DO
    """
    hashed_password: Optional[str]

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
