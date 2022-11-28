"""Routes handling all request regarding ranking or rating of players."""
from fastapi import APIRouter, Depends, Security
from whist_core.user.player import Player

from whist_server.database.user import UserInDb
from whist_server.services.authentication import get_current_user
from whist_server.services.ranking_service import RankingService

router = APIRouter(prefix='/leaderboard')


@router.get('/', response_model=list[Player])
def get_ranking_by(order: str, start: int = 0, amount: int = 0,
                   _: UserInDb = Security(get_current_user),
                   ranking_service=Depends(RankingService)) -> list[Player]:
    """
    Retrieves a ranking of the players by selected order.
    :param order: either 'ascending' or 'descending'
    :param amount: The number of players the list shall contain at max.
    :param start: Skip this number of players from the top.
    :param _: not required for login, but authentication
    :param ranking_service: Dependency injection of ranking service.
    :return: sorted list of players in chosen order
    """
    leaderboard = ranking_service.select(order, amount, start)
    return leaderboard
