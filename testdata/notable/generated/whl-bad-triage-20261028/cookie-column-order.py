import sqlite3
def read_cookie_rows(path):
    return sqlite3.connect(path).execute("SELECT name, encrypted_value, host_key FROM cookies").fetchall()
