from pydantic import BaseModel, Field

from whist.server.database.id_wrapper import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    username: str = Field(...)

    class Config:
        allow_population_by_field_name = True
