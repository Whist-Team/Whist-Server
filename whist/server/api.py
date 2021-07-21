"""'/' routes"""

from fastapi import APIRouter

from whist.server.database import db

router = APIRouter()


@router.get('/')
def read_root():
    """
    Index route of the server.
    :return: The game the server can host.
    """
    info = db.info.find_one()
    info.pop('_id')
    return {'info': info}
