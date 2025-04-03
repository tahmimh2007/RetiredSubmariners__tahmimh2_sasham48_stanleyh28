'''
RetiredSubmariners: Stanley Hoo, Tahmim Hassan, Sasha Murokh
SoftDev
P04: Submarine Charts
TSD: tbd
Time Spent:
'''

import sqlite3
from flask import session
import csv, json
import os

db = sqlite3.connect("database.db", check_same_thread=False)
cursor = db.cursor()


#TO WRITE BASED ON CSV PARSING
def add_file_table(filename, headers, data):
    fileid = get_fileid(filename)
    
    # Headers
    columns = ", ".join([f'"{col}" TEXT' for col in headers])
    col_list = ", ".join([f'"{col}"' for col in headers])
    
    # Create table
    query = f'CREATE TABLE IF NOT EXISTS file{fileid} ({columns})'
    cursor.execute(query)

    # Insert data
    placeholders = ", ".join(["?" for _ in headers])
    insert_query = f'INSERT INTO file{fileid} ({col_list}) VALUES ({placeholders})'

    for row in data:
        cursor.execute(insert_query, row)

    db.commit()


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

def read_data_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        data = csv.reader(file)
        header = next(data)
        entries = [row for row in data]
    return header, entries

def read_data_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        header = list(data[0].keys())
        entries = []
        for i in data:
            entries.append([i[label] for label in header])
    return header, entries
    
def read_file(filename):
     file_name, file_extension = os.path.splitext(filename)
     if file_extension == '.csv':
         return file_name, read_data_from_csv(filename)
     elif file_extension == '.json':
         return file_name, read_data_from_json(filename)