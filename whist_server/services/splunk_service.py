"""Splunk Integration"""
from typing import Optional

from splunklib import client


class SplunkEvent:
    """
    Wrapper for splunk events.
    """
    def __init__(self, event: str, source: Optional[str] = None, source_type: Optional[str] = None):
        self._event = event
        self._source = source
        self._source_type = source_type

    @property
    def event(self):
        """
        Event message as string
        """
        return self._event

    @property
    def source(self):
        """
        The origin of the event.
        """
        return self._source

    @property
    def sourcetype(self):
        """
        The type of the event.
        """
        return self._source_type


class SplunkService:
    """
    Service for Splunk Integration.
    """
    _instance = None
    _service: client.Service = None

    def __new__(cls, host: str, port: int, token: str):
        if cls._instance is None:
            cls._instance = super(SplunkService, cls).__new__(cls)
            cls._service = client.connect(
                host=host,
                port=port,
                splunkToken=token)
        return cls._instance

    @classmethod
    def write_event(cls, event: SplunkEvent) -> None:
        """
        Forwards an event to Splunk
        :param event: to be forwarded
        :return: None
        """
        index = cls._service.indexes['whist_monitor']
        index.submit(event=event.event, source=event.source, sourcetype=None)
