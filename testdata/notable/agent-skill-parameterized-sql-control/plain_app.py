"""Internal reporting helper (not an agent skill); uses parameterized queries."""
import sqlite3


def count_rows(table):
    conn = sqlite3.connect("app.db")
    query = f"SELECT COUNT(*) FROM {table}"
    return conn.execute(query).fetchone()[0]
