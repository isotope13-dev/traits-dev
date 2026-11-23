import sqlite3
profile = 'Google/Chrome/User Data/Default/Cookies'
conn = sqlite3.connect(profile)
count = conn.execute('SELECT count(*) FROM cookies').fetchone()
