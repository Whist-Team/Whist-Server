"""Initializes the mongodb database"""

from whist_server.const import DATABASE_NAME
from whist_server.database.connection import get_database

db = get_database(DATABASE_NAME)
