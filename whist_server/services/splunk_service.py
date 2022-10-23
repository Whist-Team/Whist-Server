"""Splunk Integration"""
import os
from typing import Optional

from splunklib import client


class SplunkEvent:
    """
    Wrapper for splunk events.
    """

    def __init__(self, event: str, source: Optional[str] = None, source_type: Optional[str] = None):
        """
        Constructor.
        :param event: Name of the event.
        :param source: Origin of the event.
        :param source_type: Type of the origin.
        """
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
    def source_type(self):
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

    def __new__(cls):
        """Creates a new instance of this service singleton."""
        if cls._instance is None:
            cls._instance = super(SplunkService, cls).__new__(cls)

            try:
                host = os.environ['SPLUNK_HOST']
                port = int(os.environ['SPLUNK_PORT'])
                token = os.environ['SPLUNK_TOKEN']
                cls._service = client.connect(host=host, port=port, splunkToken=token)
            except KeyError:
                print('Splunk parameter are not set.')
        return cls._instance

    @property
    def available(self):
        """
        Splunk connection is available.
        """
        return self._service is not None

    @classmethod
    def write_event(cls, event: SplunkEvent) -> None:
        """
        Forwards an event to Splunk
        :param event: to be forwarded
        :return: None
        """
        index = cls._service.indexes['whist_monitor']
        index.submit(event=event.event, source=event.source, sourcetype=event.source_type)
