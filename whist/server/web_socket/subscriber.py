"""Client abstraction"""
from fastapi import WebSocket

from whist.server.web_socket.events.event import Event


# pylint: disable=too-few-public-methods
class Subscriber:
    """
    A subscriber represents one client.
    """

    def __init__(self, connection: WebSocket):
        """
        Constructor
        :param connection: Implementation of the web socket connection.
        """
        self._connection = connection

    def send(self, event: Event) -> None:
        """
        Sends one event to this client.
        :param event: Any type of event.
        :return: None
        """
        self._connection.send_json(event)
