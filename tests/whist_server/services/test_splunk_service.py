import importlib.util
import os
import unittest
from unittest.mock import MagicMock, patch

from whist_server.services.splunk_service import SplunkEvent, SplunkService


@unittest.skipIf(importlib.util.find_spec("splunklib") is None, 'Splunk not installed')
class SplunkServiceTestCase(unittest.TestCase):
    @patch.dict(os.environ, {'SPLUNK_HOST': 'localhost', 'SPLUNK_PORT': '1234', 'SPLUNK_TOKEN': 'abc'})
    def setUp(self) -> None:
        self.index_mock = MagicMock()
        self.service_mock = MagicMock(indexes={'whist_monitor': self.index_mock})
        with patch('splunklib.client.connect', return_value=self.service_mock) as self.connect_mock:
            self.service = SplunkService()

    def tearDown(self) -> None:
        SplunkService._instance = None
        SplunkService._service = None

    def test_creation(self):
        self.connect_mock.assert_called_once_with(host='localhost', port=1234, splunkToken='abc')

    def test_write_event(self):
        event = SplunkEvent(event='Start', source='Test', source_type='testing')
        self.service.write_event(event)
        self.index_mock.submit.assert_called_once_with(event=event.event, source=event.source,
                                                       sourcetype=event.source_type)

    def test_available(self):
        self.assertTrue(self.service.available)

    def test_not_available(self):
        SplunkService._instance = None
        SplunkService._service = None
        service = SplunkService()
        self.assertFalse(service.available)


@unittest.skipIf(importlib.util.find_spec("splunklib") is None, 'Splunk not installed')
class SplunkNotSupportedTestCase(unittest.TestCase):
    def test_no_service(self):
        service = SplunkService()
        self.assertIsNone(service._service)
