from typing import Optional

from pydantic import BaseModel, Field

from whist.server.database.id_wrapper import PyObjectId


class GameInfo(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    game: str
    version: str
