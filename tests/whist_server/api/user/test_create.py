from tests.whist_server.base_token_case import TestCaseWithToken


class UserTestCase(TestCaseWithToken):

    def test_post_user(self):
        """
        Tests the creation of a new user.
        """
        data = {'username': 'test', 'password': 'abc'}
        response = self.client.post(url='/user/create', json=data)
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertTrue('user_id' in response.json())
        self.user_service_mock.add.assert_called_once()

    def test_post_user_no_username(self):
        """
        Tests the creation of a new user.
        """
        data = {'password': 'abc'}
        response = self.client.post(url='/user/create', json=data)
        self.assertEqual(422, response.status_code)
        self.user_service_mock.add.assert_not_called()

    def test_post_user_no_pwd(self):
        """
        Tests the creation of a new user.
        """
        data = {'username': 'test'}

        response = self.client.post(url='/user/create', json=data)
        self.assertEqual(422, response.status_code)
        self.user_service_mock.add.assert_not_called()
        
    def test_post_user_duplicate(self):
        """
        Tests the user can be created only once.
        """
        data = {'username': 'test', 'password': 'abc'}
        _ = self.client.post(url='/user/create', json=data)
        response = self.client.post(url='/user/create', json=data)
        self.assertEqual(response.status_code, 400, msg=response.content)
        self.user_service_mock.add.assert_called_once()

