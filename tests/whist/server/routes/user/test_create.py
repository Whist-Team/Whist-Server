import unittest

from starlette.testclient import TestClient

from whist.server import app
from whist.server.database import db


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self) -> None:
        db.user.drop()

    def test_post_user(self):
        """
        Tests the creation of a new user.
        """
        data = {'username': 'test', 'password': 'abc'}
        response = self.client.post(url='/user/create/', json=data)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertDictEqual(response.json(), {'user_id': '1'})
        self.assertEqual(1, db.user.count())

    def test_post_user_no_pwd(self):
        """
        Tests the creation of a new user.
        """
        data = {'username': 'test'}
        with self.assertRaisesRegex(KeyError, 'password'):
            _ = self.client.post(url='/user/create/', json=data)
        self.assertEqual(0, db.user.count())
