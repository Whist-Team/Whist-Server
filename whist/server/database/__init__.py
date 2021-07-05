from pymongo import MongoClient

from whist.server.const import DATABASE_NAME

client = MongoClient()
db = client[DATABASE_NAME]
