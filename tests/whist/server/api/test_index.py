import unittest

import pkg_resources
from fastapi.testclient import TestClient

from whist.server import app


class IndexTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_index(self):
        """
        Test the index route returns the game whist.
        """
        whist_core_version = pkg_resources.get_distribution('whist-core').version
        whist_server_version = pkg_resources.get_distribution('whist-server').version
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(),
                             {'info': {'game': 'whist', 'whist-core': whist_core_version,
                                       'whist-server': whist_server_version}})
