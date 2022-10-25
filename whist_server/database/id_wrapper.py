"""Id object for pydantic"""
from bson import ObjectId


class PyObjectId(ObjectId):
    """
    Wraps the object id in oder to fit into pydantic's BaseModel
    """

    @classmethod
    def __get_validators__(cls):
        """Returns the class' validators."""
        yield cls.validate

    @classmethod
    def validate(cls, value):
        """
        Validates a potential object id.
        :param value: the object to validate
        :return: a object id wrapped around the value
        """
        if not ObjectId.is_valid(value):
            raise ValueError('Invalid object id')
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        """Changes the type to a string."""
        field_schema.update(type='string')
