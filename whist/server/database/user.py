from typing import Optional

from pydantic import BaseModel, Field

from whist.server.database.id_wrapper import PyObjectId
from whist.server.services.password import PasswordService


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    username: str


class UserInDb(User):
    """
    User DO
    """
    hashed_password: str

    def verify_password(self, password):
        return PasswordService.verify(password, self.hashed_password)
