"""Game models"""
from typing import Optional

from pydantic import BaseModel, Field

from whist.server.database.id_wrapper import PyObjectId
from whist.server.services.password import PasswordService


class Game(BaseModel):
    """
    Game DAO
    """
    id: Optional[PyObjectId] = Field(alias='_id')
    game_name: str


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
