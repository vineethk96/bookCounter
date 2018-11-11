#!/usr/bin/env python3
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
                self.collection = self.db['collection']
            except:
                print("Could not connect to MongoDB")
    def __del__(self):
        self.conn.drop_database('db')

    def count_book(self, book):
        record = self.collection.find_one({'Name': book['Name'], 'Author': book['Author']})
        if record is None:
            return "Error: Unable to get book stock number. Book doesn't exist"
        return "OK: " + str(record['stock']) + " books in stock"
    
    def add_book(self, book):
        count = self.collection.find({'Name': book['Name'], 'Author': book['Author']}).count()    
        if count < 1:
            book['stock'] = 0
            rec_id = self.collection.insert_one(book)

            return "OK: Successfully inserted. Book id " + str(rec_id.inserted_id)
        else:
            return "Error: Unable to add. Book already exists"
            
    def buy_book(self, book, amt):
        if not isinstance(amt, int):
            return "Error: Count must be an integer value"
        elif amt < 0:
            return "Error: Count must be a positive integer"
        record = self.collection.find_one({'Name': book['Name'], 'Author': book['Author']})
        if record is not None:
            stock = record['stock']
            stock += amt
            self.collection.update_one({'Name': book['Name'], 'Author': book['Author']},
                                       {"$set": {'stock': stock}})
            record = self.collection.find_one({'Name': book['Name'], 'Author': book['Author']})                           
            ret_value = "OK: " + str(book) + " Stock: " + str(record["stock"])
            return ret_value
        else:
            return "Error: Book doesn't exist. Please add book first"
            

    def sell_book(self, book, amt):
        if not isinstance(amt, int):
            return "Error: Count must be an integer value"
        elif amt < 0:
            return "Error: Count must be a positive integer"
        record = self.collection.find_one({'Name': book['Name'], 'Author': book['Author']})
        if record is not None:
            stock = record['stock']
            if amt <= stock:
                stock -= amt
                self.collection.update_one({'Name': book['Name'], 'Author': book['Author']},
                                           {"$set": {'stock': stock}})
                record = self.collection.find_one({'Name': book['Name'], 'Author': book['Author']})                           
                ret_value = "OK: " + str(book) + " Stock: " + str(record["stock"])
                return ret_value
            else:
                return "Error: stock is not enough"
        else:
            return "Error: Book does not exist. Please add book first"

    def delete_book(self, book):
        record = self.collection.find_one({'Name': book['Name'], 'Author': book['Author']})
        if record is not None:
            self.collection.delete_one({'Name': book['Name'], 'Author': book['Author']})
            return "OK: Successfully deleted."
        else:
            return "Error: Unable to delete. Book does not exist"
        
    def list_books(self):
        ret_array = list(self.collection.find())
        return ret_array

#    def exec_action(self, payload):
#        action = payload['Action']
#        msg = payload['Msg']
#        if action == "ADD":
#            book = msg['Book Info']
#            self.add_book(self, book)
#        elif action == 'DELETE':
#            book = msg['Book Info']
        

if __name__ == "__main__":
    print("This is StorageDB.py")
