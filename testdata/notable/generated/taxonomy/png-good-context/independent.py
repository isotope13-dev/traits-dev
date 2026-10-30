import socket, subprocess
s = socket.socket()
data = s.recv(1024)
print(data)
subprocess.call("printf ok", shell=True)
