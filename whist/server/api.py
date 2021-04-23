"""'/' routes"""

from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def read_root():
    """
    Index route of the server.
    :return: The game the server can host.
    """
    return {'game': 'whist'}
