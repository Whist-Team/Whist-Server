import os
import unittest
from unittest.mock import MagicMock, patch

from whist_server.services.splunk_service import SplunkEvent, SplunkService


class SplunkServiceTestCase(unittest.TestCase):
    @patch.dict(os.environ, {'SPLUNK_HOST': 'localhost', 'SPLUNK_PORT': '1234',
                             'SPLUNK_TOKEN': 'abc'})
    def setUp(self) -> None:
        self.index_mock = MagicMock()
        self.service_mock = MagicMock(indexes={'whist_monitor': self.index_mock})
        with patch('splunklib.client.connect', return_value=self.service_mock) as self.connect_mock:
            self.service = SplunkService()

    def tearDown(self) -> None:
        SplunkService._instance = None
        SplunkService._service = None

    @patch.dict(os.environ, {'SPLUNK_HOST': 'localhost', 'SPLUNK_PORT': '1234',
                             'SPLUNK_TOKEN': 'abc'})
    def test_write_event(self):
        event = SplunkEvent(event='Start', source='Test', source_type='testing')
        self.service.write_event(event)
        self.index_mock.submit.assert_called_once_with(event=event.event, source=event.source,
                                                       sourcetype=event.source_type)
