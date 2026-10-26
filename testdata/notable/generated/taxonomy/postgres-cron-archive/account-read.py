from pathlib import Path

def read_account(path):
    return Path(path).read_text()

records = read_account("/etc/passwd")
