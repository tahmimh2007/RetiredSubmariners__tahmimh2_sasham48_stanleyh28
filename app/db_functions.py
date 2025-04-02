<<<<<<< HEAD
import csv

def read_data(csv_file):
    with open(csv_file, 'r') as file:
        header = file.readline()
        body = file.readlines()
        print(header)
        print(body)
        
read_data('customers.csv')
=======
'''
RetiredSubmariners: Stanley Hoo, Tahmim Hassan, Sasha Murokh
SoftDev
P04: Submarine Charts
TSD: tbd
Time Spent:
'''

import sqlite3
from flask import session

db = sqlite3.connect("database.db", check_same_thread=False)
cursor = db.cursor()


'''
#TO WRITE BASED ON CSV PARSING
def add_file_table(filename,<csv>): #######
    fileid = get_fileid(filename)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS file{fileid}(#######)")
    db.commit()
'''

def add_user(username, password):
    cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password))
    db.commit()


def get_users():
    return cursor.execute("SELECT username FROM users").fetchall()

def get_id(username):
    return cursor.execute(f"SELECT id FROM users WHERE username='{username}'").fetchone()[0]

def get_password(username):
    return cursor.execute(f"SELECT password FROM users WHERE username='{username}'").fetchone()[0]

def validate_user(username, password): #returns true/false
    users = [user[0] for user in get_users()]
    if username not in users:
        return False
    dbPassword = get_password(username)
    if dbPassword:
        return (dbPassword==password)
    return False

def get_files(username): #returns all filenames belonging to a specific user
    userid = get_id(username)
    return cursor.execute("SELECT filename FROM files WHERE userid='{userid}'").fetchall()

def add_files(username, filename):
    userid = get_id(username)
    cursor.execute("INSERT INTO files(filename, userid) VALUES(?, ?)", (filename, userid))
    db.commit()

def get_fileid(filename):
    return cursor.execute(f"SELECT id FROM files WHERE filename='{filename}'").fetchone()[0]
>>>>>>> eabb103d064a2703526ca65024338705ff8e2a8d
