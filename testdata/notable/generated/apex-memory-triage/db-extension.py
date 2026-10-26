import sqlite3
conn = sqlite3.connect("memory.db")
conn.load_extension("sqlite_vec.so")
