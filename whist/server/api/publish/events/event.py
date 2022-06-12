"""Abstraction of events"""
from abc import ABC

from pydantic import BaseModel


class Event(ABC, BaseModel):
    """
    It is sent via the websocket upon Game State changes.
    """
