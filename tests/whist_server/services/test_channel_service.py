import asyncio
import unittest
from unittest.mock import MagicMock, AsyncMock

from whist_server.services.channel_service import ChannelService
from whist_server.services.error import ChannelNotFoundError, ChannelAlreadyExistsError
from whist_server.web_socket.events.event import Event


class ChannelServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.channel = MagicMock(notify=AsyncMock())
        self.service = ChannelService()

    def test_notify(self):
        self.service.add('1', self.channel)
        event = Event()
        asyncio.run(self.service.notify('1', event))
        self.channel.notify.assert_called_once_with(event)

    def test_notify_removed(self):
        self.service.add('2', self.channel)
        self.service.remove('2')
        event = Event()
        with self.assertRaises(ChannelNotFoundError):
            asyncio.run(self.service.notify('2', event))

    def test_notify_not_added(self):
        event = Event()
        with self.assertRaises(ChannelNotFoundError):
            asyncio.run(self.service.notify('3', event))

    def test_remove_not_added(self):
        with self.assertRaises(ChannelNotFoundError):
            self.service.remove('3')

    def test_already_added(self):
        self.service.add('4', self.channel)
        with self.assertRaises(ChannelAlreadyExistsError):
            self.service.add('4', self.channel)
