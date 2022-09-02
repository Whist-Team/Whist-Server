"""Splunk Integration"""
from splunklib import client


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
