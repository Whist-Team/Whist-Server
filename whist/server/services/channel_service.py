from whist.server.services.error import ChannelAlreadyExistsError, ChannelNotFoundError
from whist.server.web_socket.events.event import Event
from whist.server.web_socket.side_channel import SideChannel
from whist.server.web_socket.subscriber import Subscriber


class ChannelService:
    _instance = None
    _channels: dict[str, SideChannel] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChannelService, cls).__new__(cls)
            cls._channels = {}
        return cls._instance

    @classmethod
    def add(cls, room_id: str, channel: SideChannel) -> None:
        if room_id in cls._channels.keys():
            raise ChannelAlreadyExistsError()
        cls._channels.update({room_id: channel})

    @classmethod
    def attach(cls, room_id: str, subscriber: Subscriber) -> None:
        if room_id not in cls._channels.keys():
            side_channel = SideChannel()
            cls.add(room_id, side_channel)
        cls._channels.get(room_id).attach(subscriber)

    @classmethod
    def remove(cls, room_id: str) -> None:
        if room_id not in cls._channels.keys():
            raise ChannelNotFoundError()
        cls._channels.pop(room_id)

    @classmethod
    def notify(cls, room_id: str, event: Event) -> None:
        if room_id not in cls._channels.keys():
            raise ChannelNotFoundError()
        cls._channels.get(room_id).notify(event)
