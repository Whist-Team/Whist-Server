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
    @patch('sys.argv', ['--admin_name=root', '--admin_pwd=password', 'localhost', '55368'])
    def test_cli_1(self):
        thread_start = Process(target=main, daemon=True)
        thread_start.start()
        sleep(2)
        response = httpx.get('http://localhost:55368')
        thread_start.kill()
        sleep(1)
        self.assertEqual(200, response.status_code)

    @skipIf(importlib.util.find_spec("splunklib") is None, 'Splunk not installed')
    @patch.dict(os.environ, {'SPLUNK_HOST': 'localhost', 'SPLUNK_PORT': '1234', 'SPLUNK_TOKEN': 'abc'})
    @patch('sys.argv', ['--admin_name=root', '--admin_pwd=password', 'localhost', '55369'])
    def test_cli_2(self):
        thread_start = Process(target=main, daemon=True)
        thread_start.start()
        sleep(2)
        response = httpx.get('http://localhost:55369')
        thread_start.kill()
        sleep(1)
        self.assertEqual(200, response.status_code)
