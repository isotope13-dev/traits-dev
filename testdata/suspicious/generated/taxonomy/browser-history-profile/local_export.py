import shutil
import sqlite3
from pathlib import Path
root = Path.home() / 'Google/Chrome/User Data'
shutil.copyfile(root / 'Default/History', '/tmp/history.db')
with sqlite3.connect('/tmp/history.db') as db:
    print(db.execute('SELECT url, title, visit_count FROM urls WHERE url LIKE ?', ('%example.org%',)).fetchall())
