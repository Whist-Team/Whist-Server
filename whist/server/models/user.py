from pydantic import BaseModel, Field

from whist.server.models.py_object_id import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    username: str = Field(...)

    class Config:
        allow_population_by_field_name = True
