from typing import Optional

from pydantic import BaseModel, Field

from whist.server.database.id_wrapper import PyObjectId


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    username: str
