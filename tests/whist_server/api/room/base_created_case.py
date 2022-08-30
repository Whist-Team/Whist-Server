from unittest.mock import MagicMock

from tests.whist_server.base_token_case import TestCaseWithToken


class BaseCreateGameTestCase(TestCaseWithToken):
    def setUp(self) -> None:
        super().setUp()
        self.room_mock = MagicMock(id='1', start=MagicMock(), ready_player=MagicMock())
        self.room_service_mock.get = MagicMock(return_value=self.room_mock)
