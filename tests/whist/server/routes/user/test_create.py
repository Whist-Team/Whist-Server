import unittest

from starlette.testclient import TestClient

from whist.server import app


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_post_user(self):
        """
        Tests the creation of a new user.
        """
        data = {'username': 'test'}
        response = self.client.post(url='/user/create/', json=data)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertDictEqual(response.json(), {'user_id': '1'})
