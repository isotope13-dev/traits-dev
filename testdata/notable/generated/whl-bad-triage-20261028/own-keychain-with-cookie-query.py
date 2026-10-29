import subprocess

def query_application_session(db):
    secret = subprocess.run(["security", "find-generic-password", "-w", "-s", "MyApp Token"], capture_output=True)
    return db.execute("SELECT name, value, hex(encrypted_value) FROM cookies").fetchall(), secret.stdout
