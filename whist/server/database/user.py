"""User models"""
from typing import Any

from whist.core.user.player import Player

from whist.server.const import INITIAL_RATING
from whist.server.services.password import PasswordService


class UserInDb(Player):
    """
    User DO
    """
    hashed_password: str

    def __init__(self, rating=INITIAL_RATING, **data: Any):
        super().__init__(rating=rating, **data)

    def verify_password(self, password) -> bool:
        """
        Verifies the password for a specific user.
        :param password: plain text of the password
        :return: True if verified else False
        """
        return PasswordService.verify(password, self.hashed_password)

    def to_user(self) -> Player:
        """
        Converts the DO to DAO.
        :return: User with no password saved in object.
        """
        return Player(**self.dict())
