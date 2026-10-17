import os
import psycopg
with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    conn.execute("SELECT current_timestamp")
