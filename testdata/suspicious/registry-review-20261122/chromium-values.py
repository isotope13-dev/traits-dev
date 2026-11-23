import sqlite3
profile = 'Google/Chrome/User Data/Default/Login Data'
conn = sqlite3.connect(profile)
rows = conn.execute('SELECT origin_url, username_value, password_value FROM logins').fetchall()
