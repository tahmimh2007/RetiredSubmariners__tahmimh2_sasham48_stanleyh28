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
import re
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DB_DIR = os.path.join(BASE_DIR, "data")
# os.makedirs(DB_DIR, exist_ok=True)  # Make sure the folder exists

# DB_PATH = os.path.join(DB_DIR, 'database.db')
# print("DB_PATH:", DB_PATH)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

#Initialize tables
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

#Add a new file table called file[id], where id corresponds to fileid in files
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

# Deletes old table
def delete_table(username, filename):
    conn = get_db_connection()
    cur = conn.cursor()
    file_id = get_file_id(username, filename)
    cur.execute(f"DROP TABLE IF EXISTS file{file_id};")
    conn.commit()
    conn.close()

def update_file(username, filename, headers, data):
    delete_table(username, filename)
    add_file_table(username, filename, headers, data)

#create new user
def add_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(username, password_hash) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

#get list of all users
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    users = cur.execute("SELECT username FROM users").fetchall()
    conn.close()
    return users

#get user id from username
def get_user_id(username):
    conn = get_db_connection()
    cur = conn.cursor()
    user = cur.execute("SELECT user_id FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return user[0] if user else None

#get list of all files associated with username
def get_files(username):
    conn = get_db_connection()
    cur = conn.cursor()
    user_id = get_user_id(username)
    if user_id is None:
        return []
    filenames = cur.execute("SELECT filename FROM files WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return [file[0] for file in filenames]

#add a new file for the user in files in order to get a unique fileid
def add_file(username, filename):
    conn = get_db_connection()
    cur = conn.cursor()
    user_id = get_user_id(username)
    if user_id is not None:
        cur.execute("INSERT INTO files(filename, user_id) VALUES(?, ?)", (filename, user_id))
        conn.commit()
    conn.close()

#get file id from files
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

        # Not in list format yet
        if data[0] != '[':
            # in format {...}, {...}, etc
            if re.findall('''["']data["']:''', data) == []:
                backslash = "\\"
                data_list = f'''[{', '.join(data.split('{backslash}n')).strip()[:-1]}]'''
                json_data = json.loads(data_list)
            # in format {'headers': {...}, 'data': {...}}
            else:
                json_data = json.loads(data)['data']
                print(json_data)
        # Converts string to json format
        else:
            json_data = json.loads(data)
        header = list(json_data[0].keys()) if json_data else []
        # print(header)
        entries = [[item[key] for key in header] for item in json_data]
        return header, entries
    except:
        return None, None

# Returns headers and entries of uploaded file to save
def save_data(data, file_extension):
    if file_extension == 'csv':
        return save_csv_data(data)
    elif file_extension == 'json':
        return save_json_data(data)



def splice_headings(headings):
    return[h.strip() for h in headings.split(',') if h.strip()]

# For csv files (manual)
def save_csv_data_manual(data, headings):
    try:
        # Converts string to csv format
        csv_file = io.StringIO(data)
        csv_data = csv.reader(csv_file)
        col_count = len(next(csv_data, []))
        header = splice_headings(headings)
        if len(header)!=col_count:
            flash(f"Invalid number of headings for this csv! You have {col_count} columns but only {len(header)} headings!", 'error')
            return None, None, False
        csv_data = csv.reader(csv_file)
        entries = [row for row in csv_data]
        return header, entries, True
    except:
        flash("File is not valid CSV!", 'error')
        return None, None, False

# For json files (manual)
def save_json_data_manual(data, headings):
    try:
        # Not in list format yet
        if data[0] != '[':
            # in format {...}, {...}, etc
            if re.findall('''["']data["']:''', data) == []:
                backslash = "\\"
                data_list = f'''[{', '.join(data.split('{backslash}n')).strip()[:-1]}]'''
                json_data = json.loads(data_list)
            # in format {'headers': {...}, 'data': {...}}
            else:
                json_data = json.loads(data)['data']
                print(json_data)
        # Converts string to json format
        else:
            json_data = json.loads(data)
        # print(json_data)
        # print(json_data[0])
        # print(json_data[0].keys())
        header = headings
        if json_data and len(header) != len(json_data[0]):
            flash(f"Invalid number of headings for this csv! You have {len(json_data[0])} columns but only {len(header)} headings!", 'error')
            return None, None, False
        # print(header)
        entries = [[item[key] for key in header] for item in json_data]
        return header, entries, True
    except:
        return None, None, False

# Returns headers and entries of uploaded file to save (manual)
def save_data_manual(data, file_extension, headings):
    if file_extension == 'csv':
        return save_csv_data_manual(data, headings)
    elif file_extension == 'json':
        return save_json_data_manual(data, headings)




def get_headers(file_id): ###should work
    conn = get_db_connection()
    cur = conn.cursor()
    headers = cur.execute(f"SELECT * FROM pragma_table_info('file{file_id}')").fetchall()
    headers = [header['name'] for header in headers]
    conn.close()
    return headers

def get_headers_float(file_id): ###returns numberical headers
    conn = get_db_connection()
    cur = conn.cursor()
    columns_info = cur.execute(f"PRAGMA table_info('file{file_id}')").fetchall()
    column_names = [col[1] for col in columns_info]
    headers = []

    for col in column_names:
        values = cur.execute(f"SELECT {col} FROM file{file_id}").fetchall()
        values = [v[0] for v in values if v[0] is not None]

        all_float = True
        for val in values:
            try:
                float(val)
            except (ValueError, TypeError):
                all_float = False
                break

        if all_float and values:
            headers.append(col)
    conn.close()
    return headers

def get_headers_nonfloat(file_id):  ### returns non-numerical headers
    conn = get_db_connection()
    cur = conn.cursor()
    columns_info = cur.execute(f"PRAGMA table_info('file{file_id}')").fetchall()
    column_names = [col[1] for col in columns_info]
    headers = []

    for col in column_names:
        values = cur.execute(f"SELECT {col} FROM file{file_id}").fetchall()
        values = [v[0] for v in values if v[0] is not None]

        all_float = True
        for val in values:
            try:
                float(val)
            except (ValueError, TypeError):
                all_float = False
                break

        if not all_float and values:
            headers.append(col)
    conn.close()
    return headers

def get_filename(file_id):
    conn = get_db_connection()
    cur = conn.cursor()
    filename = cur.execute("SELECT * FROM files WHERE file_id=?", (file_id,)).fetchone()
    conn.close()
    return filename

def get_x(file_id, field): #THIS MIGHT WORK I HAVENT TESTED IT YET
    conn = get_db_connection()
    cur = conn.cursor()
    output = cur.execute(f"SELECT * FROM file{file_id}").fetchall()
    try:
        output = [float(out[field]) for out in output]
    except (ValueError, TypeError):
        output = [out[field] for out in output]

    conn.close()
    return output

def get_y(file_id, fields): #fields is a list, THIS MIGHT WORK I HAVENT TESTED IT YET
    conn = get_db_connection()
    cur = conn.cursor()
    output = []
    for field in fields:
        temp = cur.execute(f"SELECT * FROM file{file_id}").fetchall()
        temp = [float(t[field]) for t in temp]
        output += [temp]
    conn.close()
    return output

#registers a user
def register_user():
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
