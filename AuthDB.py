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
    def __del__(self):
        self.conn.drop_database('db')
    def add_user(self, user, password):
        new_user = {'username': user, 'password': password}
        record = self.collection.find_one(new_user)
        if record is None:
            self.collection.insert_one(new_user)
            return "Successfully added user " + user
        return "User " + user + " already exists"
    def authenticate(self, username, password):
        credentials = {'username': username, 'password': password}
        record = self.collection.find_one(credentials)
        if record is None:
            return False
        return True

