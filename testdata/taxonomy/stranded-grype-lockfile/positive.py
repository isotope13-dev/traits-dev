import sqlite3
connection = sqlite3.connect(":memory:")
connection.executescript("CREATE TABLE users (id INTEGER, password TEXT);")
dataset_path = "data/events.parquet"
