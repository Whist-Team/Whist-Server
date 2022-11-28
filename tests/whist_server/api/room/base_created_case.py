from unittest.mock import MagicMock

from tests.whist_server.base_token_case import TestCaseWithToken


class BaseCreateGameTestCase(TestCaseWithToken):
    def setUp(self) -> None:
        super().setUp()
        table_mock = MagicMock(users=MagicMock(players=[self.player_mock.to_player()]))
        self.room_mock = MagicMock(id='1', room_name='test_room', start=MagicMock(),
                                   ready_player=MagicMock(), table=table_mock)
        self.room_service_mock.get = MagicMock(return_value=self.room_mock)
