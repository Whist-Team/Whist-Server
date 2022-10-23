"""Side Channel Manager"""
from whist_server.services.error import ChannelAlreadyExistsError, ChannelNotFoundError
from whist_server.web_socket.events.event import Event
from whist_server.web_socket.side_channel import SideChannel
from whist_server.web_socket.subscriber import Subscriber


class ChannelService:
    """
    Manages websocket side-channel clients
    """
    _instance = None
    _channels: dict[str, SideChannel] = None

    def __new__(cls):
        """Creates a new instance of this service singleton."""
        if cls._instance is None:
            cls._instance = super(ChannelService, cls).__new__(cls)
            cls._channels = {}
        return cls._instance

    @classmethod
    def add(cls, room_id: str, channel: SideChannel) -> None:
        """
        Adds a side-channel to the service.
        :param room_id: ID of the room the side-channel is associated with
        :param channel: the side-channel wrapper
        :return: None
        """
        if room_id in cls._channels.keys():
            raise ChannelAlreadyExistsError()
        cls._channels.update({room_id: channel})

    @classmethod
    def attach(cls, room_id: str, subscriber: Subscriber) -> None:
        """
        Adds a client to a side-channel.
        :param room_id: ID of the room the side-channel is associated with
        :param subscriber: the client wrapper
        :return: None
        """
        cls._channels.get(room_id).attach(subscriber)

    @classmethod
    def remove(cls, room_id: str) -> None:
        """
        Removes a side-channel from the service.
        :param room_id: ID of the room the side-channel is associated with
        :return: None
        """
        if room_id not in cls._channels.keys():
            raise ChannelNotFoundError()
        cls._channels.pop(room_id)

    @classmethod
    async def notify(cls, room_id: str, event: Event) -> None:
        """
        Multicast to all clients of a room.
        :param room_id: ID of the room the side-channel is associated with
        :param event: the wrapped information of what to broadcast
        :return: None
        """
        if room_id not in cls._channels.keys():
            raise ChannelNotFoundError()
        await cls._channels.get(room_id).notify(event)
