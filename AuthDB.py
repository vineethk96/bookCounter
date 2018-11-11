import sys
from pymongo import MongoClient


class DataBase:
    def __init__(self, host = None, port = None):
        if host is None and port is None:
            try:
                self.conn = MongoClient()
                self.db = self.conn['db']
                self.collection = self.db['collection']
            except:
                print("Could not connect to MongoDB")
        else:
            self.host = host
            self.port = port
            try:
                self.conn = MongoClient(host, port)
                self.db = self.conn['db']
                self.collection = self.db['users']
            except:
                print("Could not connect to MongoDB")
    def add_user(self, user, password):
        new_user = {'username': user, 'password': password}
        self.collection.insert_one(new_user)
        print("added user " + user)
    def authenticate(self, username, password):
        credentials = {'username': username, 'password': password}
        record = self.collection.find_one(credentials)
        if record is None:
            return False
        return True


if __name__ == "__main__":
    print("This is AuthDB.py")
