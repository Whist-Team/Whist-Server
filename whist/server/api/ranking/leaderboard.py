from fastapi import APIRouter, Depends
from whist.core.user.player import Player

from whist.server.services.ranking_service import RankingService

router = APIRouter(prefix='/leaderboard')


@router.get('/{order}', response_model=list[Player])
def get_ranking_by(order: str, ranking_service=Depends(RankingService)) -> list[Player]:
    """
    Retrieves a ranking of the players by selected order.
    :param order: either 'ascending' or 'descending'
    :param ranking_service: Dependency injection of ranking service.
    :return: sorted list of players in chosen order
    """
    leaderboard = ranking_service.all(order)
    return leaderboard
