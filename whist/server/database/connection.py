import pymongo

from whist.server.const import DATABASE_NAME, TEST_DATABASE


def get_database():
    client = pymongo.MongoClient()
    if DATABASE_NAME == TEST_DATABASE:
        client.drop_database(DATABASE_NAME)
    return client[DATABASE_NAME]
