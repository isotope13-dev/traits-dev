import sqlite3, requests
schema_tables = ["ZWAMESSAGE", "ZWAMEDIAITEM"]
con = sqlite3.connect("local.db")
rows = con.execute("SELECT * FROM settings").fetchall()
requests.post("https://telemetry.example/status", data="ready")
