import sqlite3
from database import connect

def register_user(username, password):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?,?)",
                    (username, password))
        conn.commit()
        return True
    except:
        return False


def login_user(username, password):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                (username, password))

    return cur.fetchone()