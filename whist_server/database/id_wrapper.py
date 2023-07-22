"""Id object for pydantic"""
from typing import Any, Annotated, Union

from bson import ObjectId
from pydantic import PlainSerializer, AfterValidator, WithJsonSchema


def validate_object_id(value: Any) -> ObjectId:
    """
    Validates an id for a pymongo object.
    :param value: value to be validated
    :return:
    """
    if isinstance(value, ObjectId):
        return value
    if ObjectId.is_valid(value):
        return ObjectId(value)
    raise ValueError("Invalid ObjectId")


# This can be used as an ID in BaseModels that are fed to a pymongo instance.
# https://stackoverflow.com/a/76722139/421615
PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),  # pylint: disable=W0108
    WithJsonSchema({"type": "string"}, mode="serialization"),
]
