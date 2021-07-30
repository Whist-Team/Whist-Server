"""User models"""
from typing import Optional

from pydantic import BaseModel, Field

from whist.server.database.id_wrapper import PyObjectId
from whist.server.services.password import PasswordService


class User(BaseModel):
    """User DAO"""
    id: Optional[PyObjectId] = Field(alias='_id')
    username: str


class UserInDb(User):
    """
    User DO
    """
    hashed_password: str

    def verify_password(self, password):
        """
        Verifies the password for a specific user.
        :param password: plain text of the password
        :return: True if verified else False
        """
        return PasswordService.verify(password, self.hashed_password)
