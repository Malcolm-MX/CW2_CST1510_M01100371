import sqlite3

DB_PATH = 'DATA\project_data.db'

def connect_database():
    return sqlite3.connect(DB_PATH)