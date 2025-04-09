import unittest

import importlib.metadata
from fastapi.testclient import TestClient

from whist_server import app


class IndexTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_index(self):
        """
        Test the index route returns the game whist.
        """
        whist_core_version =  importlib.metadata.version('whist-core')
        whist_server_version = importlib.metadata.version('whist-server')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(),
                             {'info': {'game': 'whist', 'whist-core': whist_core_version,
                                       'whist-server': whist_server_version}})

    def test_favicon(self):
        response = self.client.get('/favicon.ico')
        self.assertEqual(response.status_code, 200)
