'''
RetiredSubmariners: Stanley Hoo, Tahmim Hassan, Sasha Murokh
SoftDev
P04: Submarine Charts
TSD: tbd
Time Spent:
'''

from db_functions import get_db_connection

#user table
def user_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    conn.commit()
    conn.close()

#files table
def files_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS files(id INTEGER PRIMARY KEY, filename TEXT NOT NULL UNIQUE, userid INTEGER)")
    conn.commit()
    conn.close()
