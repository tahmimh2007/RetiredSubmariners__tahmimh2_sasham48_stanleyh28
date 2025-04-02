'''
RetiredSubmariners: Stanley Hoo, Tahmim Hassan, Sasha Murokh
SoftDev
P04: Submarine Charts
TSD: tbd
Time Spent:
'''

import sqlite3
from flask import session

#connects to SQLite database, creates if not already made
db = sqlite3.connect("database.db", check_same_thread=False)
cursor = db.cursor()

#user table
def user_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    db.commit()

#files table
def files_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS files(id INTEGER PRIMARY KEY, filename TEXT NOT NULL UNIQUE, userid INTEGER)")
    db.commit()

user_table()
files_table()
