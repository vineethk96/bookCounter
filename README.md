# Assignment 3

## Libraries Used
|AuthDB.py|service.py|StorageDB.py|storage.py|LED_PWM.py|led.py|
|:-:|:-:|:-:|:-:|:-:|:-:|
|||sys|flask||sys|
|||pymongo|socket|RPi.GPIO|socket|
||||zeroconf|time|logging|
|||||time|
|||||zeroconf|



## AuthDB.py
### Author
Mohammad Aarij
## service.py
### Author
Mohammad Aarij
## StorageDB.py
### Author
Sajan Ronvelwala
### Description
This file encapsulates the MongoDB database used to store book information.
### Usage
The hostname and port number are taken in as arguments, but are set for local hosting by default. An example of creating a local MongoDB connection using this class:
```example_db = DataBase()```
### DataBase Functions
The ```book``` argument is taken in as a dictionary.
1. count_book(book)
    * Counts stock number of a specified book.
    * Returns an error if the book does not exist in the database.
2. add_book(book)
    * Adds a database entry for the given book.
    * Returns an error if there is already an entry for the book.
3. buy_book(book, amt)
    * Increases stock for specified book by given amount, ```amt```. 
    * Returns an error if there is no database entry for the given book or an invalid amount argument is given.
4. sell_book(book, amt)
    * Used after sales are made. Decreases stock for specified book by given amount, ```amt```. 
    * Returns an error if there is no database entry for the given book, an invalid amount argument is given or if there is not enough stock for the sale.
5. del_book(book)
    * Deletes the specified book.
    * Returns an error if the book does not exist in the database.
6. list_books()
    * Returns a list of all books in the collection.

For more information about this program, open a Python3 interpreter prompt and
type ```import StorageDB```, followed by ```help(StorageDB)```.


## storage.py
### Author
Sajan Ronvelwala
### Description
This script runs a Flask server and provides a RESTful interface to the book database at the same time as advertising itself using Zeroconf.
### Structure
One function encapsulates the configurations for the setting up a Zeroconf service.
To provide the RESTful interface, a function is written for each of the database API functions to route queries accordingly.
The script registers the Zeroconf service first, and then runs the Flask server.

For more information about this program, open a Python3 interpreter prompt and
type ```import storage```, followed by ```help(storage)```.

## LED_PWM.py
### Author
Vineeth Kirandumkara
## led.py
### Author
Vineeth Kirandumkara