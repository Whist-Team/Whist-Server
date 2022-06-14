"""Abstraction of events"""
from abc import ABC

from pydantic import BaseModel
from whist.core.user.player import Player


class Event(ABC, BaseModel):
    """
    It is sent via the websocket upon Game State changes.
    """


class PlayerJoined(Event):
    """
    It is sent when a player joins a game.
    """
    player: Player
