import sqlite3


def search_users(name):
    connection = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE name = {name}"
    return connection.execute(query).fetchall()
