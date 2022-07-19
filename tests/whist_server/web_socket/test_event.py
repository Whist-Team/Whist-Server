from unittest import TestCase

from whist_core.cards.card import Card, Suit, Rank
from whist_core.user.player import Player
from whist_server.web_socket.events.event import PlayerJoinedEvent, RoomStartedEvent, \
    CardPlayedEvent


class EventTestCase(TestCase):
    def setUp(self) -> None:
        self.card = Card(suit=Suit.CLUBS, rank=Rank.NUM_8)
        self.player = Player(username='ititus', rating=100)

    def test_player_joined(self):
        event = PlayerJoinedEvent(player=self.player)
        self.assertIsNotNone(event.json())

    def test_player_joined_name(self):
        event = PlayerJoinedEvent(player=self.player)
        self.assertEqual('PlayerJoinedEvent', event.name)

    def test_room_started_name(self):
        event = RoomStartedEvent()
        self.assertEqual('RoomStartedEvent', event.name)

    def test_card_played(self):
        event = CardPlayedEvent(card=self.card, player=self.player)
        self.assertIsNotNone(event.json())

    def test_card_played_name(self):
        event = CardPlayedEvent(card=self.card, player=self.player)
        self.assertEqual('CardPlayedEvent', event.name)
