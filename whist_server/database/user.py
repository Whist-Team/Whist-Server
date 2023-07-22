"""User models"""
from typing import Any, Optional

from pydantic import model_validator, Field, ConfigDict
from whist_core.user.player import Player

from whist_server.const import INITIAL_RATING
from whist_server.database.id_wrapper import PyObjectId
from whist_server.services.password import PasswordService


class UserInDb(Player):
    """
    User DO
    """
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    hashed_password: Optional[bytes] = None
    github_id: Optional[str] = None
    github_username: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # pylint: disable=no-self-argument
    @model_validator(mode="before")
    @classmethod
    def validate_password_sso(cls, values):
        """
        Checks if the user is SSO or password based.
        :param values:
        :return:
        """
        if values.get('hashed_password') is None and values.get('github_username') is None:
            raise ValueError('User must be either SSO or have a password.')
        return values

    def __init__(self, rating=INITIAL_RATING, **data: Any):
        """
        Constructor.
        :param rating: The start value of the player's rating.
        :param data: dict with 'games' key for amount of games already played
        """
        super().__init__(rating=rating, **data)

    def verify_password(self, password) -> bool:
        """
        Verifies the password for a specific user.
        :param password: plain text of the password
        :return: True if verified else False
        """
        return PasswordService.verify(password, self.hashed_password)

    def to_player(self) -> Player:
        """
        Converts the DO to DAO.
        :return: User with no password saved in object.
        """
        return Player(**self.dict())
