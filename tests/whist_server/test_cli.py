import importlib.util
import os
from multiprocessing import Process
from time import sleep
from unittest import TestCase, skipIf
from unittest.mock import patch

import httpx
import pytest

from whist_server.cli import main


@pytest.mark.integtest
class CliTestCase(TestCase):
    @patch('sys.argv', ['--reload', '--admin_name=root', '--admin_pwd=password', '0.0.0.0', '8080'])
    def test_cli_1(self):
        thread_start = Process(target=main, daemon=True)
        thread_start.start()
        sleep(1)
        response = httpx.get('http://0.0.0.0:8080')
        thread_start.terminate()
        self.assertEqual(200, response.status_code)

    @skipIf(importlib.util.find_spec("splunklib") is None, 'Splunk not installed')
    @patch.dict(os.environ, {'SPLUNK_HOST': 'localhost', 'SPLUNK_PORT': '1234', 'SPLUNK_TOKEN': 'abc'})
    @patch('sys.argv', ['--reload', '--admin_name=root', '--admin_pwd=password', '0.0.0.0', '8080'])
    def test_cli_2(self):
        thread_start = Process(target=main, daemon=True)
        thread_start.start()
        sleep(1)
        response = httpx.get('http://0.0.0.0:8080')
        thread_start.terminate()
        self.assertEqual(200, response.status_code)
