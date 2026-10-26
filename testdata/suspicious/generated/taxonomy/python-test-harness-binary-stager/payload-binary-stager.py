import os

SCRIPT = """
with open(path, "wb") as f:
    f.write(data)
"""

payload = fetch_update()
write_blob(payload, SCRIPT)
os.chmod(path, 0o755)
launch(path)
