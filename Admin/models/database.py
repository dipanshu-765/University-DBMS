import pymongo


class Database:
    db = pymongo.MongoClient()

    @staticmethod
    def initialize(uri):
        client = pymongo.MongoClient(uri)
        Database.db = client['tdu']
        print(f"Initialized Database {Database.db}")