from multiprocessing import Process
from time import sleep
from unittest import TestCase
from unittest.mock import patch

import httpx
import pytest

from whist_server.cli import main


@pytest.mark.integtest
class CliTestCase(TestCase):
    @patch('sys.argv', ['--reload', '--admin_name=root', '--admin_pwd=password', '0.0.0.0', '8080'])
    def test_cli(self):
        thread_start = Process(target=main, daemon=True)
        thread_start.start()
        sleep(1)
        response = httpx.get('http://0.0.0.0:8080')
        thread_start.terminate()
        thread_start.join()
        self.assertEqual(200, response.status_code)
