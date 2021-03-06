import unittest
from unittest.mock import patch

from bson import ObjectId

from whist_server.database.id_wrapper import PyObjectId


class PyObjectIdTestCase(unittest.TestCase):
    @patch.object(ObjectId, 'is_valid')
    def test_not_validate(self, is_valid_mock):
        is_valid_mock.return_value = False

        ob_id = PyObjectId()
        with self.assertRaises(ValueError):
            PyObjectId.validate(ob_id)

    def test_validate(self):
        id_object = PyObjectId()
        validated_object = PyObjectId.validate(id_object)
        self.assertIsInstance(validated_object, ObjectId)
