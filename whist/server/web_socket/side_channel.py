"""Handles push of events"""
from pydantic import BaseModel

from whist.server.web_socket.events.event import Event
from whist.server.web_socket.subscriber import Subscriber


class SideChannel(BaseModel):
    """
    Connection to a client that pushes event regarding Game State Changes.
    """
    subscriber = []

    # pylint: disable=too-few-public-methods
    class Config:
        """
        Configuration class that allows arbitrary types as fields.
        """
        arbitrary_types_allowed = True

    def attach(self, subscriber: Subscriber) -> None:
        """
        Adds a client to this channel.
        :param subscriber: client that wants to listen on the stream.
        :return: None.
        """
        self.subscriber.append(subscriber)

    def remove(self, subscriber: Subscriber) -> None:
        """
        Removes a client from this channel.
        :param subscriber: client that does not want to listen on the stream anymore.
        :return: None.
        """
        self.subscriber.remove(subscriber)

    def notify(self, event: Event) -> None:
        """
        Sends one event to all client that have subscribed.
        :param event: Event to be sent to all clients.
        :return: None
        """
        for subscriber in self.subscriber:
            subscriber.send(event)
