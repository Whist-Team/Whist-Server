import unittest
from unittest.mock import MagicMock, patch

from whist_server.services.splunk_service import SplunkEvent, SplunkService


class SplunkServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.index_mock = MagicMock()
        self.service_mock = MagicMock(indexes={'whist_monitor': self.index_mock})

    def test_write_event(self):
        event = SplunkEvent(event='Start', source='Test', source_type='testing')
        with patch('splunklib.client.connect', return_value=self.service_mock):
            service = SplunkService('localhost', 7000, 'abc')
            service.write_event(event)
            self.index_mock.submit.assert_called_once_with(event=event.event, source=event.source,
                                                           sourcetype=event.source_type)
