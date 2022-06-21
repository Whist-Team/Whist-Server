"""DAO of game info"""

from pydantic import BaseModel


# DAO
# pylint: disable=too-few-public-methods
class GameInfo(BaseModel):
    """
    Contains meta data of the server.
    """
    game: str
    version: str
