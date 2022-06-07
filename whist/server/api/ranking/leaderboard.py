from fastapi import APIRouter
from whist.core.user.player import Player

from whist.server.services.ranking_service import RankingService

router = APIRouter(prefix='/leaderboard')


@router.get('/{order}', response_model=list[Player])
def get_ranking_by(order: str) -> list[Player]:
    """
    Retrieves a ranking of the players by selected order.
    :param order: either 'ascending' or 'descending'
    :return: sorted list of players in chosen order
    """
    ranking_service = RankingService()
    leaderboard = ranking_service.all(order)
    return leaderboard
