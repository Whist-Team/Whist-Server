"""Initializes the mongodb database"""

from whist.server.const import DATABASE_NAME
from whist.server.database.connection import get_database

db = get_database(DATABASE_NAME)
