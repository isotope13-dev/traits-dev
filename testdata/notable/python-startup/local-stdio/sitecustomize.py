import socket
import subprocess
peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer.connect(("127.0.0.1", 8125))
peer.sendall(b"startup:1|c")
with open("/dev/null", "r+") as local:
    subprocess.Popen(["/bin/sh"], stdin=local, stdout=local, stderr=local)
