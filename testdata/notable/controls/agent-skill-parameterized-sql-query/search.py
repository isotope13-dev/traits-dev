import sqlite3


def search_users(name):
    connection = sqlite3.connect("users.db")
    query = "SELECT * FROM users WHERE name = ?"
    return connection.execute(query, (name,)).fetchall()
