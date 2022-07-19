"""Handles push of events"""

from whist_server.web_socket.events.event import Event
from whist_server.web_socket.subscriber import Subscriber


class SideChannel:
    """
    Connection to a client that pushes event regarding Game State Changes.
    """
    subscriber = []

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

    async def notify(self, event: Event) -> None:
        """
        Sends one event to all client that have subscribed.
        :param event: Event to be sent to all clients.
        :return: None
        """
        for subscriber in self.subscriber:
            await subscriber.send(event)
