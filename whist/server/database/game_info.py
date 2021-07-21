"""DAO of game info"""
from typing import Optional

from pydantic import BaseModel, Field

from whist.server.database.id_wrapper import PyObjectId


# DAO
# pylint: disable=too-few-public-methods
class GameInfo(BaseModel):
    """
    Contains meta data of the server.
    """
    id: Optional[PyObjectId] = Field(alias='_id')
    game: str
    version: str
