"""Interaction with the current trick of a room."""
from typing import Union

from fastapi import APIRouter, BackgroundTasks, Security, Depends
from fastapi import status
from whist_core.cards.card import Card
from whist_core.cards.card_container import OrderedCardContainer
from whist_core.cards.card_container import UnorderedCardContainer
from whist_core.game.errors import NotPlayersTurnError
from whist_core.game.player_at_table import PlayerAtTable
from whist_core.game.warnings import TrickNotDoneWarning

from whist_server.api.util import create_http_error
from whist_server.database.user import UserInDb
from whist_server.services.authentication import get_current_user
from whist_server.services.channel_service import ChannelService
from whist_server.services.room_db_service import RoomDatabaseService
from whist_server.web_socket.events.event import CardPlayedEvent, TrickDoneEvent

router = APIRouter(prefix='/room/trick')


@router.get('/hand/{room_id}', status_code=200, response_model=UnorderedCardContainer)
def hand(room_id: str, user: UserInDb = Security(get_current_user),
         room_service=Depends(RoomDatabaseService)) -> UnorderedCardContainer:
    """
    Returns the current hand of player.
    :param room_id: unique identifier for which the player's hand is requested
    :param user: for which the hand is requested
    :param room_service: Injection of the room database service. Requires to interact with the
    database.
    :return: UnorderedCardContainer containing all cards of the player
    """
    room = room_service.get(room_id)

    player = room.get_player(user)
    return player.hand


# Most of them are injections.
# pylint: disable=too-many-arguments
@router.post('/play_card/{room_id}', status_code=200, response_model=OrderedCardContainer)
def play_card(room_id: str, card: Card, background_tasks: BackgroundTasks,
              user: UserInDb = Security(get_current_user),
              room_service=Depends(RoomDatabaseService),
              channel_service: ChannelService = Depends(ChannelService)) -> OrderedCardContainer:
    """
    Request to play a card for a given room.
    :param room_id: at which table the card is requested to be played
    :param card: which is requested to be played
    :param background_tasks: asynchronous handler
    :param user: who played a card
    :param room_service: Injection of the room database service. Requires to interact with the
    database.
    :param channel_service: Injection of the websocket channel manager.
    :return: the stack after card being played if successful. If not the players turn raises error.
    """
    room = room_service.get(room_id)
    trick = room.current_trick()

    try:
        player = room.get_player(user)
        trick.play_card(player=player, card=card)
        room_service.save(room)
        background_tasks.add_task(channel_service.notify, room_id,
                                  CardPlayedEvent(card=card, player=user.to_player()))
        if trick.done:
            background_tasks.add_task(channel_service.notify, room_id,
                                      TrickDoneEvent(winner=trick.winner))
    except NotPlayersTurnError as turn_error:
        message = f'It is not {user.username}\'s turn'
        raise create_http_error(message, status.HTTP_400_BAD_REQUEST) from turn_error
    return trick.stack.model_dump(mode='json')


@router.get('/winner/{room_id}', status_code=200,
            response_model=Union[PlayerAtTable, dict[str, str]])
def get_winner(room_id: str, user: UserInDb = Security(get_current_user),
               room_service=Depends(RoomDatabaseService)) -> Union[PlayerAtTable, dict[str, str]]:
    """
    Requests the winner of the current stack.
    :param room_id: for which the stack is requested
    :param user: who requested the winner
    :param room_service: Injection of the room database service. Requires to interact with the
    database.
    :return: The PlayerAtTable object of the winner. Raises Exception if the user has not joined
    the room yet. Replies with a warning if the trick has not be done.
    """
    room = room_service.get(room_id)
    if user not in room.players:
        message = 'You have not joined the table.'
        raise create_http_error(message, status.HTTP_403_FORBIDDEN)

    trick = room.current_trick()
    try:
        winner = trick.winner
    except TrickNotDoneWarning:
        return {'status': 'The trick is not yet done, so there is no winner.'}
    return winner.model_dump(mode='json')
