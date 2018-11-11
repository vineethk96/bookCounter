from flask import Flask, request
import socket
from zeroconf import ServiceInfo, Zeroconf

from StorageDB import DataBase

###############################################################################
# Flask Server

app = Flask(__name__)
database = DataBase()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("google.com", 80))
ip = s.getsockname()[0]


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

###############################################################################
# Zeroconf

def get_zeroconf_info():
    ''' Returns zeroconf service info.'''
    desc = {"path" : "storage"}

    info = ServiceInfo("_http._tcp.local.",
                       "Team 7's Storage._http._tcp.local.",
                       socket.inet_aton(ip), 5000, 0, 0, desc,
                       "Team7-Storage.local.")
    return info

if __name__ == '__main__':
    zeroconf = Zeroconf()
    info = get_zeroconf_info()
    zeroconf.register_service(info)
    try:
        app.run(host=ip, debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.unregister_service(info)
        del(database)
