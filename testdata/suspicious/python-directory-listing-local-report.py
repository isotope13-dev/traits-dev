import os
import socket

files = os.listdir(".")
listing = "\n".join(files)
print(f"Files in directory:\n{listing}")

with socket.create_connection(("127.0.0.1", 43935), timeout=10):
    pass
