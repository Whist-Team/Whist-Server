from bson import ObjectId


class PyObjectId(ObjectId):
    """

    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid object id')
        return ObjectId(v)

    @classmethod
    def __modify_schema(cls, field_schema):
        field_schema.update(type='string')
