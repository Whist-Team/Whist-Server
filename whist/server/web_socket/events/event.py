"""Abstraction of events"""
from abc import ABC

from pydantic import BaseModel
from whist.core.user.player import Player


class Event(ABC, BaseModel):
    """
    It is sent via the websocket upon Game State changes.
    """

    @property
    def name(self):
        """
        Returns the class name of the event.
        """
        return self.__class__.__name__


class PlayerJoined(Event):
    """
    It is sent when a player joins a game.
    """
    player: Player
