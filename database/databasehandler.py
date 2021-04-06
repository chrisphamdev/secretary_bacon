from tinydb import TinyDB, Query

# process the custom database
db = TinyDB('database/currencydb.json')
database = Query()

# each member will be store in the data base under the
# form 'userid balance' seperated by a space
def read_database():
    with open('currencydb.txt', 'r') as file:
        database_raw = file.read().split('\n')
        database = {}
        for user in database:
            pass