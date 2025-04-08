'''
RetiredSubmariners: Stanley Hoo, Tahmim Hassan, Sasha Murokh
SoftDev
P04: Submarine Charts
TSD: tbd
Time Spent:
'''

import sqlite3
from flask import session, request, flash
import csv, json
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
print("DB_PATH:", DB_PATH)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS files(
            id INTEGER PRIMARY KEY, 
            filename TEXT NOT NULL UNIQUE, 
            userid INTEGER
        );
    ''')

    conn.commit()
    conn.close()

def add_file_table(filename, headers, data):
    conn = get_db_connection()
    cur = conn.cursor()
    fileid = get_fileid(filename)
    
    columns = ", ".join([f'"{col}" TEXT' for col in headers])
    col_list = ", ".join([f'"{col}"' for col in headers])
    
    query = f'CREATE TABLE IF NOT EXISTS file{fileid} ({columns})'
    cur.execute(query)

    placeholders = ", ".join(["?" for _ in headers])
    insert_query = f'INSERT INTO file{fileid} ({col_list}) VALUES ({placeholders})'

    for row in data:
        cur.execute(insert_query, row)

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    users = cur.execute("SELECT username FROM users").fetchall()
    conn.close()
    return users

def get_id(username):
    conn = get_db_connection()
    cur = conn.cursor()
    user = cur.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return user[0] if user else None

def get_password(username):
    conn = get_db_connection()
    cur = conn.cursor()
    user = cur.execute("SELECT password FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return user[0] if user else None

def validate_user(username, password):
    db_password = get_password(username)
    if db_password:
        return check_password_hash(db_password, password)
    return False

def get_files(username):
    conn = get_db_connection()
    cur = conn.cursor()
    userid = get_id(username)
    if userid is None:
        return []
    files = cur.execute("SELECT filename FROM files WHERE userid=?", (userid,)).fetchall()
    conn.close()
    return files

def add_files(username, filename):
    conn = get_db_connection()
    cur = conn.cursor()
    userid = get_id(username)
    if userid is not None:
        cur.execute("INSERT INTO files(filename, userid) VALUES(?, ?)", (filename, userid))
        conn.commit()
    conn.close()

def get_fileid(filename):
    conn = get_db_connection()
    cur = conn.cursor()
    file = cur.execute("SELECT id FROM files WHERE filename=?", (filename,)).fetchone()
    conn.close()
    return file[0] if file else None

def read_data_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        data = csv.reader(file)
        header = next(data)
        entries = [row for row in data]
    return header, entries

def read_data_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        header = list(data[0].keys()) if data else []
        entries = [[item[key] for key in header] for item in data]
    return header, entries

def read_file(filename):
    file_name, file_extension = os.path.splitext(filename)
    if file_extension == '.csv':
        return file_name, read_data_from_csv(filename)
    elif file_extension == '.json':
        return file_name, read_data_from_json(filename)

def register_user():
    create_tables()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        try:
            add_user(username, password_hash)
            flash('Registration successful! Please login here!', 'success')
            return 'success'
        except Exception as e:
            flash('Username already exists!', 'error')
            return 'fail'
