import unittest

from starlette.testclient import TestClient

from whist_server import app
from whist_server.database import db


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
        response = self.client.post(url='/user/create', json=data)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertTrue('user_id' in response.json())
        self.assertEqual(1, db.user.estimated_document_count())

    def test_post_user_no_username(self):
        """
        Tests the creation of a new user.
        """
        data = {'password': 'abc'}
        response = self.client.post(url='/user/create', json=data)
        self.assertEqual(422, response.status_code)
        self.assertEqual(0, db.user.estimated_document_count())

    def test_post_user_no_pwd(self):
        """
        Tests the creation of a new user.
        """
        data = {'username': 'test'}
        response = self.client.post(url='/user/create', json=data)
        self.assertEqual(422, response.status_code)
        self.assertEqual(0, db.user.estimated_document_count())
