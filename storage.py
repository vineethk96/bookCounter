from zeroconf import ServiceInfo, Zeroconf
from flask import Flask, request

from StorageDB import DataBase

app = Flask(__name__)
database = DataBase()

@app.route("/book/add", methods=["POST"])
def add():
    ''' Adds book to the database.'''
    book = request.get_json()
    return str(database.add_book(book))

@app.route("/book/delete", methods=["DELETE"])
def delete():
    ''' Deletes books from the database.'''
    book = request.get_json()
    return str(database.delete_book(book))

@app.route("/book/buy", methods=["PUT"])
def buy():
    ''' Increases the stock for a book in the database.'''
    info = request.get_json()
    book = {"Name" : info["Name"], "Author" : info["Author"]}
    try:
        amount = int(info["Count"])
    except TypeError:
        amount = info["Count"] # database will handle the error
    return str(database.buy_book(book, amount))

@app.route("/book/sell", methods=["PUT"])
def sell():
    ''' Decreases the stock for a book in the database.'''
    info = request.get_json()
    book = {"Name" : info["Name"], "Author" : info["Author"]}
    try:
        amount = int(info["Count"])
    except TypeError:
        amount = info["Count"] # database will handle the error
    return str(database.sell_book(book, amount))

@app.route("/book/count", methods=["GET"])
def count():
    ''' Retrieves the count/stock of the specified book in the database.'''
    name = request.args.get("Name")
    author = request.args.get("Author")
    book = {"Name" : name, "Author" : author}
    return str(database.count_book(book))

@app.route("/book/list", methods=["GET"])
def list():
    ''' Retrieves a list of all of the books in the database.'''
    book_list = database.list_books()
    value = {"Books" : book_list,
             "Msg" : "Ok. Get " + str(len(book_list)) + " books' information"}
    return str(value)

if __name__ == '__main__':
    try:
        app.run(host='localhost', debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        del(database)
