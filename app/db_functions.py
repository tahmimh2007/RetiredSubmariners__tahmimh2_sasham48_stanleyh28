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
import io
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
print("DB_PATH:", DB_PATH)

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DB_DIR = os.path.join(BASE_DIR, "data")
# os.makedirs(DB_DIR, exist_ok=True)  # Make sure the folder exists

# DB_PATH = os.path.join(DB_DIR, 'database.db')
# print("DB_PATH:", DB_PATH)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS files(
            file_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            filename TEXT NOT NULL, 
            user_id INTEGER NOT NULL
        );
    ''')

    conn.commit()
    conn.close()

def add_file_table(username, filename, headers, data):
    conn = get_db_connection()
    cur = conn.cursor()
    file_id = get_file_id(username, filename)
    
    columns = ", ".join([f'"{col}" TEXT' for col in headers])
    col_list = ", ".join([f'"{col}"' for col in headers])
    
    query = f'CREATE TABLE IF NOT EXISTS file{file_id} ({columns})'
    cur.execute(query)

    placeholders = ", ".join(["?" for _ in headers])
    insert_query = f'INSERT INTO file{file_id} ({col_list}) VALUES ({placeholders})'

    for row in data:
        cur.execute(insert_query, tuple(row))

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(username, password_hash) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    users = cur.execute("SELECT username FROM users").fetchall()
    conn.close()
    return users

def get_user_id(username):
    conn = get_db_connection()
    cur = conn.cursor()
    user = cur.execute("SELECT user_id FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return user[0] if user else None

def get_files(username):
    conn = get_db_connection()
    cur = conn.cursor()
    userid = get_user_id(username)
    if userid is None:
        return []
    files = cur.execute("SELECT filename FROM files WHERE userid=?", (userid,)).fetchall()
    conn.close()
    return files

def add_file(username, filename):
    conn = get_db_connection()
    cur = conn.cursor()
    user_id = get_user_id(username)
    if user_id is not None:
        cur.execute("INSERT INTO files(filename, user_id) VALUES(?, ?)", (filename, user_id))
        conn.commit()
    conn.close()

def get_file_id(username, filename):
    conn = get_db_connection()
    cur = conn.cursor()
    user_id = get_user_id(username)
    file = cur.execute("SELECT file_id FROM files WHERE (user_id, filename)=(?, ?)", (user_id, filename)).fetchone()
    conn.close()
    return file[0] if file else None

# For csv files
def save_csv_data(data):
    try:
        # Converts string to csv format
        csv_file = io.StringIO(data)
        csv_data = csv.reader(csv_file)
        header = next(csv_data)
        entries = [row for row in csv_data]
        return header, entries
    except:
        flash("File is not valid CSV!", 'error')
        return None, None

# For json files
def save_json_data(data):
    try:
        # Converts string to json format
        json_data = json.loads(data)
        header = list(json_data[0].keys()) if json_data else []
        entries = [[item[key] for key in header] for item in json_data]
        return header, entries
    except:
        flash("File is not valid JSON!", 'error')
        return None, None

# Returns headers and entries of uploaded file to save
def save_data(data, file_extension):
    if file_extension == 'csv':
        return save_csv_data(data)
    elif file_extension == 'json':
        return save_json_data(data)

def register_user():
    create_tables()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        try:
            add_user(username, password_hash)
            return 'success'
        except:
            return 'fail'

# authenticates a user
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        # Retrieve hashed password for the given username
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        user_row = cur.fetchone()
        conn.close()

        # Checks hashed user password against database
        if user_row and check_password_hash(user_row['password_hash'], password):
            session['username'] = username
            flash('Login successful!', 'success')
        else:
            flash('Invalid username or password!', 'error')