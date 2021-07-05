import unittest

import mongomock
from fastapi.testclient import TestClient

from whist.server import app


@mongomock.patch(servers='mongodb://localhost:27017')
class IndexTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_index(self):
        """
        Test the index route returns the game whist.
        """

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'info': {'game': 'whist', 'version': '1.0.0'}})
