import unittest

from fastapi.testclient import TestClient

from whist.server import app


class IndexTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_index(self):
        """
        Test the index route returns the game whist.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'game': 'whist'})
