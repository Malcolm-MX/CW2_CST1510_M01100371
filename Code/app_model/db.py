import sqlite3

#path to the sqlite database file
DB_PATH = 'DATA\project_data.db'

def connect_database():
    #creates a connection each time it's called back to the path as well
    return sqlite3.connect(DB_PATH)