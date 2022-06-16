from unittest.mock import MagicMock

from tests.whist.server.base_token_case import TestCaseWithToken


class BaseCreateGameTestCase(TestCaseWithToken):
    def setUp(self) -> None:
        super().setUp()
        self.game_mock = MagicMock(id='1', start=MagicMock(), ready_player=MagicMock())
        self.game_service_mock.get = MagicMock(return_value=self.game_mock)
