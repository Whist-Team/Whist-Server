from pymongo import MongoClient

mongo_client = MongoClient()
db = mongo_client['whist']
db.create_collection('user')
