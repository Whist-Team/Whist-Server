"""Connection to mongodb instance"""
import pymongo

from whist.server.const import TEST_DATABASE


def get_database(database):
    """
    Returns the mongo database.
    """
    client = pymongo.MongoClient(host=database)
    if database == TEST_DATABASE:
        client.drop_database(database)
    return client[database]
