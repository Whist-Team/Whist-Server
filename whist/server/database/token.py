"""Token models"""
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """
    DO of a token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    DAO of a token. Is linked to a user.
    """
    username: Optional[str] = None
