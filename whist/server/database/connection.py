"""Connection to mongodb instance"""
import pymongo


def get_database(database):
    """
    Returns the mongo database.
    """
    client = pymongo.MongoClient(host=database)
    return client[database]
