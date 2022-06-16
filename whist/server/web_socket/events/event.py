"""Abstraction of events"""

from pydantic import BaseModel
from whist.core.cards.card import Card
from whist.core.user.player import Player


class Event(BaseModel):
    """
    It is sent via the websocket upon Game State changes.
    """

    @property
    def name(self):
        """
        Returns the class name of the event.
        """
        return self.__class__.__name__


class CardPlayedEvent(Event):
    """
    It is sent when a player plays card.
    """
    card: Card
    player: Player


class PlayerJoinedEvent(Event):
    """
    It is sent when a player joins a game.
    """
    player: Player


class RoomStartedEvent(Event):
    """
    It is sent when a room has been started.
    """
