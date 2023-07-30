import pytest
from bson import ObjectId
from pydantic import TypeAdapter, ConfigDict

from whist_server.database.id_wrapper import PyObjectId


@pytest.mark.parametrize("obj", ["64b7992ba8f08069073f1055", ObjectId("64b7992ba8f08069073f1055")])
def test_pyobjectid_validation(obj):
    ta = TypeAdapter(PyObjectId, config=ConfigDict(arbitrary_types_allowed=True))
    ta.validate_python(obj)


@pytest.mark.parametrize("obj", ["64b7992ba8f08069073f105", ObjectId("64b7992ba8f08069073f1055")])
def test_pyobjectid_validation_invalid(obj):
    ta = TypeAdapter(PyObjectId, config=ConfigDict(arbitrary_types_allowed=True))
    with pytest.raises(ValueError):
        ta.validate_python(obj)


@pytest.mark.parametrize("obj", ["64b7992ba8f08069073f1055", ObjectId("64b7992ba8f08069073f1055")])
def test_pyobjectid_serialization(obj):
    ta = TypeAdapter(PyObjectId, config=ConfigDict(arbitrary_types_allowed=True))
    ta.dump_json(obj)
