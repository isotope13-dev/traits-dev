import shutil
from pathlib import Path
root = Path.home() / 'Google/Chrome/User Data'
shutil.copyfile(root / 'Default/History', '/tmp/history.db')
# SELECT url, title, visit_count FROM urls WHERE url LIKE ?
